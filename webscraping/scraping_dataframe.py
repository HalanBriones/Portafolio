from browser import website_connection, get_text_element
import pandas as pd
import re
from selenium.webdriver.common.by import By

print('Clean Data and make a DataFrame') 
#****************WEB SCRAPING AND DATAFRAME CREATION**********#
URL_CRITICS= 'https://www.metacritic.com/news/' #Critics games,movies,shows
website = website_connection(URL_CRITICS)
clean_data = []
try:
    for i in range(0,3):
        content = website.find_elements(By.CSS_SELECTOR,'div.c-seoArticleSummary--latest')
        for e in content:
            rawString = get_text_element(e)
            rawString = re.sub(r"[\n\t]*","",rawString) #remove tabs and new lines
            rawString = re.sub('[ ]{2,}',"",rawString) #remove double or multiple spaces
            clean_data.append(rawString) #add data to a list
        button = website.find_element (By.CSS_SELECTOR, "div.c-pageArticleListings_seeMore")
        button.click()
    website.quit()
except Exception as e:
    print(f'The Error is: {e} \n PLEASE TRY AGAIN')
#**********Split content in two list*********#
title = []
date_posted = []
for i in range(len(clean_data)):
    split_string = clean_data[i].split('.',1) #split by the dot because I found a possible pattern in the data
    title.append(split_string[0]) #list with the titles and info
    date_posted.append(split_string[1]) #list with the dated posted
#*********Creation of Dictionary*********#
data_dictionary = []
for i in range(len(title)):
    data_dictionary.append({'Title':title[i],'Date Posted':date_posted[i]})
#*********Creation of DataFrame*********#
df = pd.DataFrame(data_dictionary,columns=('Title','Date Posted'))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print('DataFrame with the latest news from Metacritic \n ',df)
#*********save dataframe to a CSV file*********#
df.to_csv("../webscraping/latesNews.csv",sep=',')#creation of the doc in the same folder
#*********read the csv doc into a new dataframe*********#
dfIN = pd.read_csv('../webscraping/latesNews.csv',skiprows=1,names=('Title','Date Posted'), index_col=None)
print('\n First 2 rows of the DataFrame: \n',dfIN.head(2))
print('\n Last 2 rows of the DataFrame: \n',dfIN.tail(2))