from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
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
        options = webdriver.ChromeOptions()
        
        # Headless configuration
        if os.getenv('HEADLESS') == '1':
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Essential Docker settings
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Anti-detection configuration
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        
        # Set Chrome binary location
        options.binary_location = os.getenv('CHROME_BIN')

        try:
            self.driver = webdriver.Chrome(
                options=options,
                driver_executable_path='/usr/local/bin/chromedriver' 
            )
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

    def get_soup(self, url, presence_selector_tuple, timeout):
        element_block = None
        try:
            self.driver = self.init_driver()
            self.driver.get(url)
            
            if os.getenv('PRINT_SELENIUM_PAGES') == '1':
                print(f"Fetched URL: {url}")
                print(self.driver.page_source[:1000])
                
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(presence_selector_tuple)
            )
            print(f"[{self.source_name}] SUCCESS! Selenium cards found for: {url}")
            element_block = element.get_attribute("outerHTML")
        except Exception as e:
            print(f"[{self.source_name}] Failed to get elements: {url} - {str(e)[:60]}")
        finally:
            self.dispose_driver()
            return BeautifulSoup(element_block, 'html.parser') if element_block else None

    def save_job(self, job_data):
        # Existing save_job implementation remains unchanged
        company, _ = Company.objects.get_or_create(name=job_data['company'])
        # ... rest of save_job logic ...

    @abstractmethod
    def scrape(self):
        """Implement in child classes"""
        pass
