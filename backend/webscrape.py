from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver_path = 'C:\\Users\\ianke\\Desktop\\chromeDriver\\chromedriver-win64\\chromedriver.exe'
url = "https://www.investing.com/economic-calendar/"


options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')  # Avoid sandboxing issues
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Set up the ChromeDriver service
service = Service(driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

try:
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'economicCalendarData')))
except:
    driver.quit()
    exit()

rows = table.find_elements(By.TAG_NAME, "tr")

data = []
headers = ['Time', 'Currency', 'Importance', 'Event', 'Actual', 'Forecast', 'Previous']

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) < 7:
        continue
    currency = cells[1].text.strip()
    if  currency == 'USD':
        row_data = {
            'Time': cells[0].text.strip(),
            'Currency':  currency,
            'Importance': cells[2].text.strip(),
            'Event': cells[3].text.strip(),
            'Actual': cells[4].text.strip(),
            'Forecast': cells[5].text.strip(),
            'Previous': cells[6].text.strip()
        }
        data.append(row_data)

driver.quit()


csv_filename = "usd_economic_calendar_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
