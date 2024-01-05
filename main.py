import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
from io import StringIO

standing_url = "https://fbref.com/en/comps/9/2015-2016/schedule/2015-2016-Premier-League-Scores-and-Fixtures"
data = requests.get(standing_url)  # downloads html from the page's url

soup = BeautifulSoup(data.text, 'html.parser')  # pursing page to help understand and makes it easier to work on it
standings_table = soup.select('table.stats_table')[0]  # here I am getting the table from the page from which I will gain informations about matches I need

links = standings_table.find_all('a')
links = [l.get("href") for l in links]  # removing anything from list that is not href value
links = [l for l in links if '/matches/' in l]
links = [l for l in links if not '/matches/2015' in l]
links = [l for l in links if not '/matches/2016' in l]
team_urls = [f"https://fbref.com{l}" for l in links]  # adding first part of urls to receive actual links
# print(*team_urls, sep='\n')


match_url = team_urls[0]
print(match_url)
match_data = requests.get(match_url)

# match = pd.read_html(StringIO(str(match_data.text)), match="Manchester Utd Player Stats")

soup = BeautifulSoup(match_data.text, 'html.parser')
performance_table = soup.select('table.stats_table')
performance_table = [s for s in performance_table if 'keeper_stats' not in s]
print(performance_table)

stats = pd.read_html(StringIO(str(performance_table)))
print(stats)
