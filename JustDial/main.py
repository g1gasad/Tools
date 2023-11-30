from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time 

path = "E:\Projects\Automations\WEBDRIVER\chromedriver.exe"

option = webdriver.ChromeOptions()
option.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=option)

driver.get("https://wap.justdial.com/analytics/enquiries?el=0&nh=1&rootvc=0&docid=9999PX771.X771.150630125848.H5Q6&hide_header=1&m=1&mobile=8390005813&old=1&source=77&tab=enquiries&wap=77&tab=enquiries")

height = driver.execute_script("return document.body.scrollHeight")
# print(height)
i = 0
while i != 2:
    containers = driver.find_elements(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    i += 1

print(len(containers))

titles = []
locations = []
date_times = []
descriptions = []
sources = []
names = []

for container in containers:
    title = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//div[@class="lead_slide_infobig font15 fw600 color414"]').text
    location = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//span[@class="infosml_loct fw700"]').text
    date_time = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//span[@class="infosml_time"]').text
    description = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//div[@class="lead_slide_descr_text pb-10 font13 fw400 color414"]').text
    source = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//div[@class="userinfo_name font13 fw600 color414 mb-10"]').text
    name = container.find_element(by='xpath', value='//div[@class="lead_slide lead_slide--missed p-15"]//div[@class="userinfo_name font13 fw600 color414"]').text
    # source = container.find_element(by='xpath', value='.//div[@class="userinfo_name font13 fw600 color414 mb-10"]').text
    titles.append(title)
    locations.append(location)
    date_times.append(date_time)
    descriptions.append(description)
    sources.append(source)
    names.append(name)
    
df = pd.DataFrame(
                {
                    'Title': titles,
                    'Location': locations,
                    'Date and Time': date_times,
                    'Description': descriptions,
                    'Source': sources,
                    'Name': names
            }
)
print(df)
driver.quit()
