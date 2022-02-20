import requests
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd


URL = "https://www.cowracouncil.com.au/Development/Public-exhibition-Development-Applications"
DATABASE = "data.sqlite"
DATA_TABLE = "data"
PROCESSED_FILES_TABLE = "files_processed"
PROCESSED_FILES_COLUMN = "name"

engine = create_engine(f'sqlite:///{DATABASE}', echo=False)
pd.DataFrame(columns=[PROCESSED_FILES_COLUMN]).to_sql(PROCESSED_FILES_TABLE, con=engine, if_exists="append")




raw = requests.get(URL)
soup = BeautifulSoup(raw.content,'html.parser')

row_set = soup.find(attrs={'id':'sub-navigation-container'}).find('li').find_all('li')

data = pd.DataFrame(columns=['council_reference','address','description','date_scraped','info_url'])
date = datetime.strftime(datetime.now(),'%d-%m-%Y')
counter = 0
for row in row_set:
        info_link = row.find('a').attrs['href']
        raw = requests.get(info_link)
        soup = BeautifulSoup(raw.content,'html.parser')

        description = soup.find("h4").text.split(" - ")[1].strip()
        council_reference = soup.find("h4").text.split("-")[0].strip()
        address = soup.find("h4").text.split(" - ")[2].strip()
        data.loc[counter] = [council_reference, address, description,date,info_link]
        counter += 1
data.to_sql(DATA_TABLE,con=engine,if_exists='append',index=False)
