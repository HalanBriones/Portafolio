import re
from selenium.webdriver import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from browser import website_connection, get_text_element

#URL'S that I worked with
URL_CRITICS= 'https://www.metacritic.com/news/' #Critics games,movies,shows
URL_HIKES = 'https://www.hikingproject.com/' #Hikings website
URL_Traveling = 'https://www.travellerspoint.com/forum.cfm?ForumID=5'

#******search content**************#
try:
    website_search = website_connection(URL_HIKES)
    search_icon = website_search.find_element(By.CSS_SELECTOR,'input[placeholder="Find trails, cities, etc"]')
    search_icon.send_keys('whistler') #Search Hikes in Whistler
    search_icon.send_keys(Keys.ENTER) #you also can do it identifying the button and use button.click()
    print('Search completed succesfully')
    website_search.quit()
except Exception as e:
    print(f'The Error is: {e} \n PLEASE TRY AGAIN')
#***********WEB SCRAPING 3 DIFERENT SITES************#
while True:
    option = input('Please select your website: \n [1] Travellerspoint \t [2] Metacritic \t [3] GSmarena \t [4] Exit \n')
    if option == '1':
        website = website_connection(URL_Traveling)
        print('First Website Travellerspoint')
        try:
            for i in range(0, 3):  # loop for 3 pages
                print(f'Page {i + 1} *****')
                content = website.find_elements(By.CSS_SELECTOR, '.forum_row')
                for e in content:
                    rawString = get_text_element(e)
                    rawString = re.sub(r"[\n\t]*", "", rawString)  # remove tabs and new lines
                    rawString = re.sub('[ ]{2,}', "", rawString)  # remove 1+ spaces
                    print(rawString.strip())  # print the list clean of spaces from both ends
                    print('*' * 10)
                button = website.find_element(By.CSS_SELECTOR, ".icon-right-open")
                button.click()  # Click in the next button and go to next page
            website.quit()#close the tab instead of leaving it open until the program finish
        except Exception as e:
            print(f'The Error is: {e} \n PLEASE TRY AGAIN')
    elif option == '2':
        website = website_connection(URL_CRITICS)
        print('Second Website Metacritic')
        try:
            for i in range(0, 3):
                print(f'Page {i + 1} *****')
                content = website.find_elements(By.CSS_SELECTOR, 'div.c-seoArticleSummary--latest')
                for e in content:
                    rawString = get_text_element(e)
                    print(rawString)
                    print('*' * 10)
                button = website.find_element(By.CSS_SELECTOR, "div.c-pageArticleListings_seeMore")
                button.click()
            website.quit()#close the tab instead of leaving it open until the program finish
        except Exception as e:
            print(f'The Error is: {e} \n PLEASE TRY AGAIN')
    elif option == '3':
        print('Third Website GSmarena')
        try:
            for i in range(0, 3):
                print(f'Page number {i + 1} *************')
                URL_PHONES = 'https://www.gsmarena.com/apple-phones-f-48-0-p' + str(i + 1) + '.php'
                website = website_connection(URL_PHONES)
                content = website.find_elements(By.CSS_SELECTOR, '.makers a')
                for e in content:
                    rawString = get_text_element(e)
                    print(rawString)
                    print('*' * 10)
                website.quit()  # close the tab instead of leaving it open until the program finish
        except Exception as e:
            print(f'The Error is: {e} \n PLEASE TRY AGAIN')
    elif option == '4': 
        print("Thank you for using the webscraping program. Goodbye!") 
        break