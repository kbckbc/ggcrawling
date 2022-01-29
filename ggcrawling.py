'''
Title : Google result page crawling
Author : BC Gwak
What to do : 
    This source code will catch URL, title, contents 
    from Google search result using BeautifulSoup 
    And insert the results into Mongodb
    Simply use it when you want to put test data into DB
Needed packages : 
    In order to use this source, install these packages.
    pip install requests
    pip install beautifulsoup4
    pip install pymongo
    pip install lxml
How to get the code : 
    git clone https://github.com/kbckbc/ggcrawling.git .
Run debug mode :
    python ggcrawling.py
Run non-debug mode :
    python -O ggcrawling.py
'''

from tkinter import E
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(host="localhost", port=27017)
db = client.chanboard
col = db.board

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
targetsite = "https://www.google.com/search?q={}&start={}"
keyword = "washu"
howmanypages = 5

for i in range(howmanypages):
    url = targetsite.format(keyword, i * 10)
    getHtml = requests.get(url, headers=header)
    bs = BeautifulSoup(getHtml.text, "lxml")
    contentLists = bs.select("div.g")

    line = 0
    for item in contentLists:
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        try:
            site = item.select_one("cite").text
            site = site[site.find("://")+3:site.find(" ", site.find("://")+3)].replace("www.", "").replace(".", "_")
            title = item.select_one("h3.LC20lb").text
            contents = item.select_one("div.IsZvec").text
            line = line+1
            if __debug__: print('''result [{}]
                utc_time: {}
                site: {}
                title: {}
                contents: {}'''.format(line, current_utc_time, site, title, contents))
            col.insert_one({
                    "name": site,
                    "title": title,
                    "contents": contents,
                    "view": 0,
                    "date": current_utc_time
                })
        except Exception as e:
            if __debug__: print(e)
            pass
