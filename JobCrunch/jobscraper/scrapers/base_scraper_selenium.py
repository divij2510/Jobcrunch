from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABC, abstractmethod
from django.utils import timezone
from jobscraper.models import Company, Job
from bs4 import BeautifulSoup
import os
import undetected_chromedriver as uc

class BaseScraperSelenium(ABC):
    def __init__(self):
        self.source_name = None
        self.base_url = None   

    def init_driver(self):
        options = uc.ChromeOptions()
        if os.getenv('HEADLESS') == '1':
            options.add_argument("--headless=new") 
            options.add_argument("--disable-gpu")
        
        # Essential for Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        options.binary_location = os.getenv('CHROME_BIN')

        try:
            self.driver = uc.Chrome(
                options=options,
                version_main=135  
            )
        except Exception as e:
            print(f"Problem when initializing UC driver: {e}")
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
            if os.getenv('PRINT_SELENIUM_PAGES')=='1':
                print(f"Fetched URL: {url}")
                print(self.driver.page_source[:1000])
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