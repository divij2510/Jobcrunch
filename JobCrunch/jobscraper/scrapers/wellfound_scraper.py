from .base_scraper_selenium import BaseScraperSelenium
from selenium.webdriver.common.by import By

class WellfoundScraper(BaseScraperSelenium):
    def __init__(self):
        super().__init__()
        self.source_name = "Wellfound"
        self.base_url = "https://wellfound.com/location/india?page="

    def scrape(self, *args, **kwargs):
        start_page = kwargs.get("start_page", 1)
        end_page = kwargs.get("end_page", 5)

        jobs = []
        for i in range(start_page, end_page):
            url = f"{self.base_url}{i}"
            try:
                page_soup = self.get_soup(url, (By.CLASS_NAME, "my-4"), 10)
                company_cards = page_soup.find_all('div', class_='mb-6')
                for card in company_cards:
                    try:
                        company_ele = card.find('h2', class_='inline text-md font-semibold')
                        company = company_ele.text.strip() if company_ele else "N/A"
                        jobs_section = card.find('div', class_='mb-4 w-full px-4')
                        if not jobs_section:
                            continue

                        job_blocks = jobs_section.find_all(recursive=False)

                        for job_block in job_blocks:
                            title_ele = job_block.find(
                                'a',
                                class_='mr-2 text-sm font-semibold text-brand-burgandy hover:underline'
                            )
                            if not title_ele:
                                continue
                            title = title_ele.text.strip()
                            apply_link = title_ele.get('href')
                            if apply_link and not apply_link.startswith(('http://', 'https://')):
                                apply_link = f"https://wellfound.com{apply_link}"

                            salary = "N/A"
                            location = "N/A"

                            for div in job_block.find_all("div", class_="flex items-center text-neutral-500"):
                                svg = div.find("svg")
                                path = svg.find("path") if svg else None
                                span = div.find("span")
                                
                                if not path or not span:
                                    continue

                                path_data = path.get("d", "")
                                if "M12.3333 7.49998" in path_data or "M10 5.83333" in path_data:
                                    salary = span.get_text(strip=True)
                                elif "M4.33333 6.17139" in path_data:
                                    location = span.get_text(strip=True)


                            job_data = {
                                'title': title,
                                'company': company,
                                'location': location,
                                'apply_link': apply_link,
                                'salary': salary,
                                'description': "N/A"
                            }
                            job = self.save_job(job_data)
                            jobs.append(job)
                    except Exception as inner_e:
                        print(f"Error parsing company card: {str(inner_e)[:80]}")
                        continue
            except Exception as e:
                print(f"Error scraping page {i}: {e}")
                continue
            print(f"[times jobs] Scraped {url} successfully!")

        self.dispose_driver()
        return jobs
