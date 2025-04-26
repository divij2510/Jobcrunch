from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")


# Initialize WebDriver
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()),options=chrome_options)

url = "https://wellfound.com/location/india?page=3"
driver.get(url)
# time.sleep(10)
try:
    ps = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.TAG_NAME,"div")))
    # print(f"found {len(ps)} jobs!")
    print(ps.text.strip())
finally:
    driver.quit()