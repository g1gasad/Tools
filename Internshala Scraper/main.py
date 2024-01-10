from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

    
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")
CHROMEDRIVER = Service("E:/Projects/WEBDRIVER/chromedriver_120.exe")


website_page = "https://internshala.com/internships/data-science-internship/"

driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
driver.get(website_page)
time.sleep(3)
# wait = WebDriverWait(driver, 100)


scroll_increment = 1000  # Adjust this value to control the scroll speed
total_scroll_distance = 17028
# page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
# print(page_height)
# Scroll in increments
for distance in range(0, total_scroll_distance, scroll_increment):
    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    time.sleep(0.1)

containers = driver.find_elements(by='xpath', value='//div[@class="container-fluid individual_internship visibilityTrackerItem "]')
print(len(containers))

names = []
companies = []
locations = []
start_dates = []
durations = []



for container in containers:
    name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').text
    company = container.find_element(by='xpath', value='.//div[@class="company_and_premium"]/a').text
    try:
        multiple_locations = []
        loc_list = container.find_elements(by='xpath', value='.//div[@id="location_names"]/span/a')
        if len(loc_list) > 1:
            for ele in loc_list:
                multiple_locations.append(ele.text)
            locations.append(multiple_locations)
        else:
            location = container.find_element(by='xpath', value='.//div[@id="location_names"]/span/a').text
            locations.append(location)
    except Exception as e:
        print(f"An Exception Error {e}")
        
    start_date = container.find_element(by='xpath', value='.//div[@id="start-date-first"]/span[2]').text
    duration = container.find_element(by='xpath', value='.//div[@class="other_detail_item "][2]/div[@class="item_body"]').text
    # name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').text
    # name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').text
    # name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').text
    
    
    
    names.append(name)
    companies.append(company)
    start_dates.append(start_date)
    durations.append(duration)



print(start_date)
# print(companies)
# print(locations)
print(durations)

driver.quit()