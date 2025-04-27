# base_scraper_selenium.py
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from abc import ABC, abstractmethod
from jobscraper.models import Company, Job
from bs4 import BeautifulSoup
import os
from django.utils import timezone

class BaseScraperSelenium(ABC):
    def __init__(self):
        self.source_name = None
        self.base_url = None
        self.driver = None

    def init_driver(self):
        options = webdriver.ChromeOptions()
        if os.getenv('HEADLESS') == '1':
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        # Essential settings for Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Anti-detection configuration
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = os.getenv('CHROME_BIN')
        # Set user-agent through CDP
        # options.aadd_cdp_option("userAgent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

        try:
            self.driver = webdriver.Chrome(options=options)
            return self.driver
        except Exception as e:
            print(f"Driver initialization failed: {str(e)[:200]}")
            raise RuntimeError("WebDriver startup failed") from e

    def dispose_driver(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            print(f"Error during driver disposal: {e}")

    def get_soup(self, url, tag_name, class_name, timeout):
        element_block = None
        try:
            self.init_driver()
            self.driver.get(url, wait_load=True)
            element_block = self.driver.page_source

            if True or os.getenv('PRINT_SELENIUM_PAGES') == '1':
                print(f"Fetched URL: {url}")
                print(element_block[:720])

            print(f"[{self.source_name}] SUCCESS! Element found for: {url}")

        except Exception as e:
            print(f"[{self.source_name}] Failed to get elements: {url} - {e}")

        finally:
            self.dispose_driver()
            return BeautifulSoup(element_block, 'html.parser').find(tag_name,class_=class_name) if element_block else None

    def save_job(self, job_data):
        company, _ = Company.objects.get_or_create(name=job_data['company'])
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
