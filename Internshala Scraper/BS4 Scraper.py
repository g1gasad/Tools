from bs4 import BeautifulSoup
import requests

link = 'https://internshala.com/internships/data-science-internship/'

response = requests.get(link)
soup = BeautifulSoup(response.content, 'html.parser')
tab_containers = soup.find_all('div', class_='container-fluid individual_internship visibilityTrackerItem ')

print(len(tab_containers))