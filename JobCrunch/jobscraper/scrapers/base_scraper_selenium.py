from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABC, abstractmethod
from django.utils import timezone
from jobscraper.models import Company, Job
from bs4 import BeautifulSoup
import os

class BaseScraperSelenium(ABC):
    def __init__(self):
        self.source_name = None
        self.base_url = None   

    

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox")  # VERY IMPORTANT for Docker
        chrome_options.add_argument("--disable-dev-shm-usage")  # IMPORTANT for Docker
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )

        try:
            self.driver = webdriver.Remote(
                command_executor=os.getenv("SELENIUM_REMOTE_URL"),
                options=chrome_options
            )
        except Exception as e:
            print(f"Problem when initializing driver: {e}")
        finally:
            return self.driver

    def dispose_driver(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error during driver disposal: {e}")


    def get_soup(self, url, presence_selector_tuple, timeout):
        element_block = None
        try:
            self.init_driver()
            self.driver.get(url)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(presence_selector_tuple)
            )
            print(f"[{self.source_name}] SUCCESS! selenium cards for: {url}!!!")
            element_block = element.get_attribute("outerHTML")
        except Exception as e:
            print(f"[{self.source_name}] Failed to get selenium cards: {url} because: {str(e)[:60]}")
        finally:
            self.dispose_driver()
            if element_block:
                return BeautifulSoup(element_block, 'html.parser')
            else:
                return None

    def save_job(self, job_data):
        company, _ = Company.objects.get_or_create(
            name=job_data['company']
        )
        try:
            job = Job.objects.get(
                source=self.source_name,
                company=company,
                location=job_data['location']
            )
        except Job.DoesNotExist:
            job = Job.objects.create(
                title=job_data['title'],
                company=company,
                salary=job_data['salary'],
                location=job_data.get('location'),
                description=job_data.get('description'),
                apply_link=job_data['apply_link'],
                source=self.source_name,
                date_posted=job_data.get('date_posted'),
                date_scraped=timezone.now()
            )
        return job

    @abstractmethod
    def scrape(self):
        """Implement in child classes"""
        pass