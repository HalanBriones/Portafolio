from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
from browser import website_connection, get_text_element

# URL NBA standings
URL_NBA = 'https://www.espn.com/nba/standings'
website = website_connection(URL_NBA)
teams = website.find_elements(By.CSS_SELECTOR,'.hide-mobile .AnchorLink')
wins = website.find_elements(By.CSS_SELECTOR,'.Table__TD:nth-child(1) .stat-cell')
loss = website.find_elements(By.CSS_SELECTOR,'.Table__TD:nth-child(2) .stat-cell')
teams_nba = []
wins_team = []
loss_team = []

#*********extracting and saving the data in 3 diferent list*********#
try:
    for e in teams:
        var = get_text_element(e)
        teams_nba.append(var)
    for e in loss:
        var =  get_text_element(e)
        loss_team.append(int(var))
    for e in wins:
        var =  get_text_element(e)
        wins_team.append(int(var))
    website.quit() #close nba website
except Exception as e:
    print(f'The Error is: {e} \n PLEASE TRY AGAIN')

dataSet = {'Teams': teams_nba,'Victories':wins_team, 'Defeats':loss_team}
df = pd.DataFrame(dataSet,columns=('Teams','Victories','Defeats'))
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#*********Creation of a list with win percentage*********#
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

#*********Graphic of victories, each team season 2025-26 until now*********#
plt.figure(figsize=(10,8))#adjust the size of the window of the graphic
plt.barh(teams_nba, wins_team)# I use barh style to be able to fit the long names of the teams
plt.xlabel('Victories')
plt.ylabel('Teams NBA')
plt.title('Victories of each NBA Team - Season 2025-26')
plt.show()