from datetime import datetime
from .base_scraper_bs4 import BaseScraperBs4

class TimesJobsScraper(BaseScraperBs4):
    def __init__(self):
        super().__init__()
        self.source_name = "TimesJobs"
        self.base_url = "https://m.timesjobs.com/mobile/jobs-search-result.html?compCluster="
    
    def scrape(self):
        results = []
        startup_list = ['Coinswitch','Myntra', 'Byjus','Shopclues.com','Razorpay','CRED','PharmEasy','Paytm','1mg','Meesho','Flipkart','Unacademy','Phonepe']
        for company in startup_list:
            soup = self.get_soup(self.base_url+company)
            job_cards = soup.find_all('div', class_='srp-job-bx')
            # print(job_cards)

            for card in job_cards:
                try:
                    # title_ele = card.find('div', class_='srp-job-heading')
                    a_tag = card.find('a')
                    title = a_tag.text.strip()
                    apply_link = a_tag.get('href')
                    company = card.find('span', class_='srp-comp-name').text.strip()
                    location= card.find('div', class_='srp-loc').text.strip()
                    salary = card.find('div',class_='srp-sal').text.strip()

                    # try:
                    #     job_soup = self.get_soup(apply_link)
                    #     if job_soup:
                    #         job_desc = job_soup.find('div', id='JobDescription')
                    #         if job_desc:
                    #             description = job_desc.get_text(separator='\n').strip()

                    #         apply_btn = job_soup.find('a', id='jdApplyButton')
                    #         if apply_btn:
                    #             from urllib.parse import urlparse, parse_qs
                    #             href = apply_btn.get('href')
                    #             query = parse_qs(urlparse(href).query)
                    #             apply_link = query.get('externalLink', [None])[0]
                    # except Exception as e:
                    #     print(f"{e} Failed fetching secondary link and description!")

                    job_data = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'apply_link': apply_link,
                        'salary': salary,
                        'description': "N/A"
                    }
                    job = self.save_job(job_data)
                    results.append(job)


                except Exception as e:
                    print(f"Error scraping job: {e}")
                    continue

        return results
