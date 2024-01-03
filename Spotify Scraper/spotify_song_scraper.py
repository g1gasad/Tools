from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

website = "https://open.spotify.com/collection/tracks"
# website = "https://www.youtube.com/"
path = "E:\Projects\WEBDRIVER\chromedriver_120.exe"

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("user-data-dir=C:/Users/CWC/AppData/Local/Google/Chrome/User Data")
OPTIONS.add_argument("--profile-directory=Default")

CHROMEDRIVER = Service("E:/Projects/WEBDRIVER/chromedriver_120.exe")
try:
    # Your script here
    driver = webdriver.Chrome(service=CHROMEDRIVER, options=OPTIONS)
    driver.get(website)
    scroll_increment = 100  # Adjust this value to control the scroll speed
    total_scroll_distance = 3000

    # Scroll in increments
    for distance in range(0, total_scroll_distance, scroll_increment):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(0.1)
    play_button_xpath = "/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div[1]/button/span"
    play_button_xpath_but = WebDriverWait(driver,50).until(lambda driver: driver.find_element("xpath", play_button_xpath))
    # time.sleep(10)

except Exception as e:
    print(f"An error occurred: {str(e)}")