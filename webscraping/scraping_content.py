import re
import pandas as pd
import matplotlib.pyplot as plt
from selenium.webdriver import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
# Function to connect to a website
def website_connexion (url):
    DRIVER_PATH    = 'C:/WebDrivers/chromedriver.exe' #location of chrome driver
    website_search = webdriver.Chrome(service=Service(DRIVER_PATH))
    website_search.get(url)
    time.sleep(1)
    return website_search


#URL'S that I worked with
URL_CRITICS= 'https://www.metacritic.com/news/' #Critics games,movies,shows
URL_HIKES = 'https://www.hikingproject.com/' #Hikings website
URL_Traveling = 'https://www.travellerspoint.com/forum.cfm?ForumID=5' #Tra
#===============
#PART A -
#===============
#******search content**************#
try:
    website_search = website_connexion(URL_HIKES)
    search_icon = website_search.find_element(By.CSS_SELECTOR,'input[placeholder="Find trails, cities, etc"]')
    search_icon.send_keys('whistler') #hikes in Burnaby
    search_icon.send_keys(Keys.ENTER) #you also can do it identifying the button and use button.click()
    print('Search completed succesfully')
    website_search.quit()
except:
    print('The search Fail')
#***********WEB SCRAPING 3 SITES************#
while True:
    option = input('Please select your website: \n [1] Travellerspoint \t [2] Metacritic \t [3] GSmarena \t [4] Exit \n')
    if option == '1':
        website = website_connexion(URL_Traveling)
        print('First Website Travellerspoint')
        try:
            for i in range(0, 3):  # loop for the 3 pages
                print(f'Page {i + 1} *****')
                content = website.find_elements(By.CSS_SELECTOR, '.forum_row')
                for e in content:
                    start = e.get_attribute('innerHTML')
                    soup = BeautifulSoup(start, features='lxml')
                    rawString = soup.get_text()
                    rawString = re.sub(r"[\n\t]*", "", rawString)  # remove tabs and new lines
                    rawString = re.sub('[ ]{2,}', "", rawString)  # remove more than 1 spaces
                    print(rawString.strip())  # print the list clean of spaces from both ends
                    print('*' * 10)
                button = website.find_element(By.CSS_SELECTOR, ".icon-right-open")
                button.click()  # Click in the next button and go to next page
            website.quit()#close the tab instead of leaving it open until the program finish
        except:
            print('This website sometimes works and sometimes doesnt due some random pop ups \n Please try again' )
    elif option == '2':
        website = website_connexion(URL_CRITICS)
        print('Second Website Metacritic')
        try:
            for i in range(0, 3):
                print(f'Page {i + 1} *****')
                content = website.find_elements(By.CSS_SELECTOR, 'div.c-seoArticleSummary--latest')
                for e in content:
                    start = e.get_attribute('innerHTML')
                    soup = BeautifulSoup(start, features='lxml')
                    print(soup.get_text())
                    print('*' * 10)
                button = website.find_element(By.CSS_SELECTOR, "div.c-pageArticleListings_seeMore")
                button.click()
            website.quit()#close the tab instead of leaving it open until the program finish
        except:
            print('This website sometimes works and sometimes doesnt due some random pop ups \n Please try again' )
    elif option == '3':
        print('Third Website GSmarena') #url number 5
        try:
            for i in range(0, 3):
                print(f'Page number {i + 1} *************')
                URL_PHONES = 'https://www.gsmarena.com/apple-phones-f-48-0-p' + str(i + 1) + '.php'
                website = website_connexion(URL_PHONES)
                time.sleep(1)
                content = website.find_elements(By.CSS_SELECTOR, '.makers a')
                for e in content:
                    start = e.get_attribute('innerHTML')
                    soup = BeautifulSoup(start, features='lxml')
                    print(soup.get_text())
                    print('*' * 10)
                website.quit()  # close the tab instead of leaving it open until the program finish
        except:
            print('This website sometimes works and sometimes doesnt due some random pop ups \n Please try again' )
    elif option == '4':  break
#*******scraping website, clean the data and transform into DataFrame*****# fROM HERE DOWN 
'''print('Clean Data and make a DataFrame with it') #USING WEBSITE metacritic
website = webdriver.Chrome(service=Service(DRIVER_PATH))
website.get(URL_CRITICS)
time.sleep(1)
clean_data = []
for i in range(0,3):
    content = website.find_elements(By.CSS_SELECTOR,'div.c-seoArticleSummary--latest')
    for e in content:
        start=e.get_attribute('innerHTML')
        soup=BeautifulSoup(start,features='lxml')
        rawString = soup.get_text()
        rawString = re.sub(r"[\n\t]*","",rawString) #remove tabs and new lines
        rawString = re.sub('[ ]{2,}',"",rawString) #remove double or multiple spaces
        clean_data.append(rawString) #add data to a list
    button = website.find_element (By.CSS_SELECTOR, "div.c-pageArticleListings_seeMore")
    button.click()
website.quit()
#**********split content of into two list*********#
title = []
date_posted = []
for i in range(len(clean_data)):
    split_string = clean_data[i].split('.') #split by the dot because I found a possible pattern in the data
    title.append(split_string[0]) #list with the titles and info
    date_posted.append(split_string[1]) #list with the dated posted
#*********creation of dictionary*********#
data_dictionary = []
for i in range(len(title)):
    data_dictionary.append({'Title':title[i],'Date Posted':date_posted[i]})
#*********Creation of DataFrame*********#
df = pd.DataFrame(data_dictionary,columns=('Title','Date Posted'))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
#*********save dataframe to a CSV file*********#
df.to_csv("latesNews.csv",sep=',')#creation of the doc in the same folder
#*********read the csv doc into a new dataframe*********#
dfIN = pd.read_csv('latesNews.csv',skiprows=1,names=('Title','Date Posted'), index_col=None)
print(dfIN.head(2))#print first 2 rows
print(dfIN.tail(2))#print last 2 rows
#===============
#PART B - Graphics
#===============
URL_NBA = 'https://www.espn.com/nba/standings' #NBA information
website = webdriver.Chrome(service=Service(DRIVER_PATH))
website.get(URL_NBA)
time.sleep(1)
teams = website.find_elements(By.CSS_SELECTOR,'.hide-mobile .AnchorLink')
wins = website.find_elements(By.CSS_SELECTOR,'.Table__TD:nth-child(1) .stat-cell')
loss = website.find_elements(By.CSS_SELECTOR,'.Table__TD:nth-child(2) .stat-cell')
teams_nba = []
wins_team = []
loss_team = []
#*********extracting and saving the data in list's*********#
for e in teams:
    start = e.get_attribute('innerHTML')
    soup = BeautifulSoup(start,features='lxml')
    var = soup.get_text()
    teams_nba.append(var)
for e in loss:
    start = e.get_attribute('innerHTML')
    soup = BeautifulSoup(start,features='lxml')
    var = soup.get_text()
    loss_team.append(var)
for e in wins:
    start = e.get_attribute('innerHTML')
    soup = BeautifulSoup(start,features='lxml')
    var = soup.get_text()
    wins_team.append(var)
website.quit() #close nba website
dataSet = {'Teams': teams_nba,'Victories':wins_team, 'Defeats':loss_team}
df = pd.DataFrame(dataSet,columns=('Teams','Victories','Defeats'))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
#*********Creation of a list of win percentage*********#
win_percentage = []
total_games = []
for i in range(len(wins_team)):
    num_games = int(wins_team[i])+int(loss_team[i])
    percentage = int(wins_team[i])/(int(wins_team[i])+int(loss_team[i]))
    win_percentage.append(round(percentage,2))
    total_games.append(num_games)
#*********adding columns to the dataframe*********#
df['Total games'] = total_games
df['Win %'] = win_percentage
#DataFrame with a aggregations
print('***DataFrame with a win percentage aggregation***\n',df)
#*********Graphic victories of each team of season 2025-26 until now*********#
plt.figure(figsize=(10,8))#adjust the size of the window of the graphic
plt.barh(teams_nba, wins_team, color='blue')# I use barh style to be able to fit the long names of the teams
plt.xlabel('Victories')
plt.ylabel('Teams NBA')
plt.title('Victories of each NBA Team - Season 2025-26')
plt.show()
'''