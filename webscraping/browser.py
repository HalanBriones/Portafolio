from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Function to connect to a website
def website_connection (url):
    DRIVER_PATH    = 'C:/WebDrivers/chromedriver.exe' #location of chrome driver in my pc
    website_search = webdriver.Chrome(service=Service(DRIVER_PATH))
    website_search.get(url)
    time.sleep(1)
    return website_search

def get_text_element(element):
    start = element.get_attribute('innerHTML')
    soup = BeautifulSoup(start, features='lxml')
    text = soup.get_text()
    return text