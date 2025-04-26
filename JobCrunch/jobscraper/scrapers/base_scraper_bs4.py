import requests
import random
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from django.utils import timezone
from jobscraper.models import Company, Job

class BaseScraperBs4(ABC):
    def __init__(self):
        self.source_name = None
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
        ]
        self.base_url = None  
    
    def _get_headers(self, referer=None):
        """Generate headers for request"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',  # Do Not Track
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        
        if referer:
            headers['Referer'] = referer
            
        return headers
    
    def get_soup(self, url, referer=None):
        """Get BeautifulSoup object from URL with delay and random user agent"""

        if referer is None and self.base_url:
            referer = self.base_url
            
        headers = self._get_headers(referer)
        response = self.session.get(url, headers=headers, timeout=30)
        
        # Check status and handle common issues
        if response.status_code == 403:
            print(f"403 Forbidden: {url}")
            
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    
    def initialize_session(self):
        if self.base_url:
            headers = self._get_headers()
            self.session.get(self.base_url, headers=headers)
    
    def save_job(self, job_data):
        company, _ = Company.objects.get_or_create(
            name=job_data['company']
        )
        
        try:
            job = Job.objects.get(  
                source=self.source_name,
                company = company,
                location = job_data['location']
            )
        except Job.DoesNotExist:  
            job = Job.objects.create( 
                title=job_data['title'],
                company=company,
                salary = job_data['salary'],
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