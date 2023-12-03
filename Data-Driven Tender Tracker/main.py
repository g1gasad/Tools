import os
from GOOGLE import Create_Service
from SCRAPER import SCRAPE_WEBPAGE_TO_DF
from SHEET_SCRAMBLER import PUSH_DATA_TO_SHEET
from SHEET_SCRAMBLER import FETCH_DATA
from SHEET_SCRAMBLER import VALIDATE_AND_UPDATE
from SCRAPER import format_scraping_time
from datetime import datetime
import time

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)   
CATALYST_SPREADSHEET_ID = '1sqQf7PtC5j4aMtYdKS4uD-ypmvuNGkP7TeQHtGENZcs'
AUTOMATION_SPREADSHEET_ID = '120Ae4G5aBSP3mTXaSrIyqt0bC__lFRzgLFVdhHc6wN4'
SLEEP_TIME = 0.3

url = input('Paste the copied Link Address of the Page:')
end_page_number = input("Enter the number of pages you want:")

SCRAPED_DF, time_elapsed = SCRAPE_WEBPAGE_TO_DF(url, end_page_number, SLEEP_TIME)
print(format_scraping_time(time_elapsed))
current_time = datetime.now().hour, datetime.now().minute
filename = f"Run Check, Time {current_time}, Rows {SCRAPED_DF.shape[0]}.xlsx"
SCRAPED_DF.to_excel(filename, index=False)

PUSH_DATA_TO_SHEET(SERVICE=service, 
                    SPREADSHEET_ID=CATALYST_SPREADSHEET_ID,
                    DATAFRAME=SCRAPED_DF, 
                    WORKSHEET_NAME_STRING="New")

old_df, new_df = FETCH_DATA(service, CATALYST_SPREADSHEET_ID, "Old", "New")

UPDATED_DF = VALIDATE_AND_UPDATE(OLD_DATAFRAME=old_df, NEW_DATAFRAME=new_df)
print('Updated df Shape: ', UPDATED_DF.shape)
print(UPDATED_DF['Updated'].value_counts())

UPDATED_DF.to_excel("Updated DF.xlsx", index=False)
# PUSH_DATA_TO_SHEET(SERVICE=service,
#                     SPREADSHEET_ID=AUTOMATION_SPREADSHEET_ID, 
#                     DATAFRAME=UPDATED_DF, 
#                     WORKSHEET_NAME_STRING="DF")

print(old_df.shape)
