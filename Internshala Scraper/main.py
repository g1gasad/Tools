from selenium import webdriver
import pandas as pd
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


website_page = "https://internshala.com/internships/data-science-internship/page-1/"

driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
driver.get(website_page)
time.sleep(3)
# wait = WebDriverWait(driver, 100)

header_string = driver.find_element(by='xpath', value='//h1[@class="heading heading_4_6 active-header page-heading"]').text
print(header_string)

# if header_string.split()[0] > 40:

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
links = []
companies = []      
locations = []
start_dates = []
durations = []
salaries = []
employment_types = []
statuses = []

for container in containers:
    name = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').text
    link = container.find_element(by='xpath', value='.//h3[@class="heading_4_5 profile"]/a').get_attribute('href')
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
    salary = container.find_element(by='xpath', value='.//span[@class="stipend"]').text
    employment_type = container.find_element(by='xpath', value='.//div[@class="other_label_container"]/div[1]/div').text
    status = container.find_element(by='xpath', value='.//div[@class="success_and_early_applicant_wrapper"]/div').text
    
    
    
    names.append(name)
    links.append(link)
    companies.append(company)
    start_dates.append(start_date)
    durations.append(duration)
    salaries.append(salary)
    employment_types.append(employment_type)
    statuses.append(status)
# print(start_dates)
# print(companies)
# print(locations)
# print(durations)
# print(salaries)
# print(links)
# print(employment_types)
# print(statuses)

driver.quit()
data = {
    "Name": names,
    "Link": links,
    "Location": locations,
    "Company": companies,
    "Start Date": start_dates,
    "Duration": durations,
    "Salary": salaries,
    "Employment Type": employment_types,
    "Status": statuses
}
df = pd.DataFrame(data)
df.to_excel("Scraper.xlsx", index=False)