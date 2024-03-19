from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

state_xpath = "//select[@name='ctl00$ContentPlaceHolder1$DropDownState']"
district_xpath = "//select[@name='ctl00$ContentPlaceHolder1$DropDownDistrict']"
sub_district_xpath = "//select[@name='ctl00$ContentPlaceHolder1$DropDownSubDistrict']"
block_xpath = "//select[@name='ctl00$ContentPlaceHolder1$DropDownBlock']"
village_xpath = "//select[@name='ctl00$ContentPlaceHolder1$DropDownVillage']"
url = "https://pmkisan.gov.in/Rpt_BeneficiaryStatus_pub.aspx"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
select_tag = soup.find('select')
select_text = select_tag.text.strip()
state_list = select_text.split("\n")[1:]

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")
CHROMEDRIVER = Service("E:/Projects/WEBDRIVER/chromedriver_122.exe")
driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
driver.get(url)
time.sleep(2)

try:
    old_state_name = None
    for state in state_list:
        new_state_name = state
        if old_state_name is None:
            state_select_element_new = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, state_xpath)))
            state_select = driver.find_element(by="xpath", value=state_xpath).click()
        else:
            state_select = driver.find_element(by="xpath", value=f"//*[contains(text(), '{old_state_name}')]").click()
        time.sleep(5)


        district_select_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, district_xpath)))
        district_selenium_list = district_select_element.find_elements(by='xpath', value=f"{district_xpath}//option")
        district_list = [d.text for d in district_selenium_list]
        old_district_name = None        
        for district in district_list[1:]:
            new_district_name = district.strip()
            time.sleep(3)
            if old_district_name is None:
                district_select_element_new = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, district_xpath)))
                district_select = driver.find_element(by="xpath", value=district_xpath).click()
            else:
                district_select = driver.find_element(by="xpath", value=f"//*[contains(text(), '{old_district_name}')]").click()
            time.sleep(3)
            district_name = driver.find_element(by='xpath', value=f"//*[contains(text(), '{new_district_name}')]")
            time.sleep(1)
            district_name.click()
            time.sleep(4)
            
        #  //////////////////////////////////////////////////////////////   
            sub_district_select_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, sub_district_xpath)))
            sub_district_selenium_list = sub_district_select_element.find_elements(by='xpath', value=f"{sub_district_xpath}//option")
            sub_district_list = [sd.text for sd in sub_district_selenium_list]
            old_sub_district_name = None
            for sub_district in sub_district_list[1:]:
                new_sub_district_name = sub_district.strip()
                time.sleep(3)
                if old_sub_district_name is None:
                    sub_district_select_element_new = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, sub_district_xpath)))
                    sub_district_select = driver.find_element(by="xpath", value=sub_district_xpath).click()
                else:
                    sub_district_select = driver.find_element(by="xpath", value=f"//*[contains(text(), '{old_sub_district_name}')]").click()
                time.sleep(3)
                sub_district_name = driver.find_element(by='xpath', value=f"//*[contains(text(), '{new_sub_district_name}')]")
                time.sleep(1)
                sub_district_name.click()
                time.sleep(4)
                
                
                block_select_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, block_xpath)))
                block_selenium_list = block_select_element.find_elements(by='xpath', value=f"{block_xpath}//option")
                block_list = [b.text for b in block_selenium_list]
                old_block_name = None
                for block in block_list[1:]:
                    new_block_name = block.strip()
                    time.sleep(3)
                    if old_block_name is None:
                        block_select_element_new = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, block_xpath)))
                        block_select = driver.find_element(by="xpath", value=block_xpath).click()
                    else:
                        block_select = driver.find_element(by="xpath", value=f"//*[contains(text(), '{old_block_name}')]").click()
                    time.sleep(3)
                    block_name = driver.find_element(by='xpath', value=f"//*[contains(text(), '{new_block_name}')]")
                    time.sleep(1)
                    block_name.click()
                    time.sleep(4)
                    
                    
                    village_select_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, village_xpath)))
                    village_selenium_list = village_select_element.find_elements(by='xpath', value=f"{village_xpath}//option")
                    village_list = [v.text for v in village_selenium_list]
                    old_village_name = None
                    for village in village_list[1:]:
                        new_village_name = village
                        time.sleep(3)
                        if old_village_name is None:
                            print('if')
                            village_select_element_new = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, village_xpath)))
                            village_select = driver.find_element(by="xpath", value=village_xpath).click()
                        else:
                            print("else")
                            village_select = driver.find_element(by="xpath", value=f"//*[contains(text(), '{old_village_name}')]").click()
                        time.sleep(3)
                        village_name = driver.find_element(by='xpath', value=f"//*[contains(text(), '{new_village_name}')]")
                        time.sleep(1)
                        village_name.click()
                        time.sleep(4)
                        
                        old_village_name = new_village_name
                        print(f"{new_block_name}: {old_village_name}")    
                    
                    
                    old_block_name = new_block_name
                    print(f"{old_block_name} iteration, Complete.")
                            
                            
                old_sub_district_name = new_sub_district_name
                print(f"{old_sub_district_name} iteration, Complete.")
            

            old_district_name = new_district_name
            # print("ODN:", old_district_name)
            print(f"{old_district_name} iteration, Complete.")
            
        old_state_name = new_state_name
        print(f"{old_state_name} iteration, Complete.")
         
         
    driver.quit()
except Exception as e:
    print('Error:', e)
finally:
    driver.quit()
