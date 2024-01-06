import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from io import StringIO

standing_url = "https://fbref.com/en/comps/9/2015-2016/schedule/2015-2016-Premier-League-Scores-and-Fixtures"
data = requests.get(standing_url)  # downloads html from the page's url

soup = BeautifulSoup(data.text, 'html.parser')  # pursing page to help understand and makes it easier to work on it
standings_table = soup.select('table.stats_table')[
    0]  # here I am getting the table from the page from which I will gain informations about matches I need

links = standings_table.find_all('a')
links = [l.get("href") for l in links]  # removing anything from list that is not href value
links = [l for l in links if '/matches/' in l]
links = [l for l in links if not '/matches/2015' in l]
links = [l for l in links if not '/matches/2016' in l]
team_urls = [f"https://fbref.com{l}" for l in links]  # adding first part of urls to receive actual links
# print(*team_urls, sep='\n')


match_url = team_urls[0]
# print(match_url)
match_data = requests.get(match_url)

soup = BeautifulSoup(match_data.text, 'html.parser')
date = soup.find('div', {'class': 'scorebox_meta'})
date_a = date.find('a')
date_text = date_a.text.strip()
# print(date_text)

date_obj = datetime.strptime(date_text, '%A %B %d, %Y')
formatted_date = date_obj.strftime('%d/%m/%Y')
print(formatted_date)

soup = BeautifulSoup(match_data.text, 'html.parser')
teams = soup.find('div', {'class': 'scorebox'})
teams_a = teams.find_all('a', href=lambda href: '/squads/' in href)
i = 1
team_one = str
team_two = str
for link in teams_a:
    team_name = link.text.strip()
    if i == 1:
        team_one = team_name
    elif i == 2:
        team_two = team_name
    i += 1


soup = BeautifulSoup(match_data.text, 'html.parser')
keeper_tables = soup.find_all('table', class_='min_width sortable stats_table min_width shade_zero')  #
for keeper_table in keeper_tables:  # in this three lines I remove goalkeepers tables
    keeper_table.decompose()  #

performance_table = soup.select('table.stats_table')

stats = pd.read_html(StringIO(str(performance_table)))
match_statistics = pd.DataFrame()
for s in range(len(stats)):
    stats[s] = stats[s].iloc[[0, -1]]
    stats[s] = stats[s].drop(0)
    stats[s].columns = stats[s].columns.droplevel()

    selected_columns = ["Sh", "SoT", "Off", "TklW", "PK", "PKatt"]
    stats[s] = stats[s][selected_columns]

    match_statistics = pd.concat([match_statistics, stats[s]])

match_statistics = match_statistics.reset_index(drop=True)

print(match_statistics)
