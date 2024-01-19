from selenium import webdriver
import pandas as pd
import time
import math
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

custom_order = {'1 day ago':3, 'Just now':0, 'Today':2, '1 week ago':10, 'Few hours ago':1,
                '4 days ago':6, '2 days ago':4, '3 days ago':5, '5 days ago':7,'7 days ago':9,
                '6 days ago':8, '2 weeks ago':11, '3 weeks ago':12, '4 weeks ago':13, '5 weeks ago':14}
    
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")
CHROMEDRIVER = Service("E:/Projects/WEBDRIVER/chromedriver_120.exe")


def scrape_data(driver):
    scroll_increment = 1000  # Adjust this value to control the scroll speed
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # print(page_height)
    for distance in range(0, page_height, scroll_increment):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(0.1)

    # This returns a list of TAB CONTAINERS
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

        try:    
            start_date = container.find_element(by='xpath', value='.//div[@id="start-date-first"]/span[2]').text
        except:
            start_date = "Could Not Fetch"

        try:
            duration = container.find_element(by='xpath', value='.//div[@class="other_detail_item "][2]/div[@class="item_body"]').text
        except:
            duration = container.find_element(by='xpath', value='.//div[@class="other_detail_item large_stipend_text"][2]/div[@class="item_body"]').text

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
    return df

website_page = "https://internshala.com/internships/apis,analytics,business-analysis,data-analysis,data-analytics,data-science,google-suite-g-suite,google-workspace,ms-sql-server,market-business-research,mysql,power-bi,programming,python,research-and-analytics,sql,selenium,sports,statistical-modeling,tableau,artificial-intelligence-internship/page-1/"

driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
driver.get(website_page)
wait = WebDriverWait(driver, 10)

header_string_xpath = '//h1[@class="heading heading_4_6 active-header page-heading"]'
def wait_for_header(header_string_xpath):
    wait.until(EC.visibility_of_element_located((By.XPATH, header_string_xpath)))

header_string = driver.find_element(by='xpath', value=header_string_xpath).text
total_posts = int(header_string.split()[0])
number_of_pages = math.ceil(total_posts/40)

df = scrape_data(driver)
if number_of_pages > 1:
    for page_number in range(2, 11):
        # website_page = f"https://internshala.com/internships/data-science-internship/page-{page_number}/"
        website_page = website_page.replace(website_page[-2], str(page_number))
        driver.execute_script("window.open('', '_blank');")
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[page_number-1])
        # Navigate to the new URL in the new tab
        driver.get(website_page)
        wait_for_header(header_string_xpath)
        new_df = scrape_data(driver)
        df = pd.concat([df, new_df], axis=0, ignore_index=True)
        time.sleep(2)


df['sorted_order'] = df['Status'].map(custom_order)
df = df.sort_values(by='sorted_order').drop('sorted_order', axis=1)
date_variable = datetime.today().date()
df.to_excel(f"{date_variable} Scraped {df.shape[0]} opportunities.xlsx", index=False)

driver.quit()
