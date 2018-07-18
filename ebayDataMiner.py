# eBay Data Miner
# By Will Greenberg
# July 17, 2018

# Purpose: Given an eBay search term, compile a list of all items with information on bid price, 
# Buy-It-Now option, time left, etc to be used for an AI system later

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import html.parser

Keywords = 'pan' #input("Enter a search term: \n")
api = Finding(appid='WillGree-Scraper-PRD-d8bba853c-c16e72d4', config_file=None)
searchRequest = { 
		'keywords':Keywords,
		'outputSelector':'SellerInfo',
		'paginationInput': [ { 'entriesPerPage':100 } ]
	}

response = api.execute('findItemsByKeywords', searchRequest)
soup = soup(response.content, "html.parser")

print(soup.text + "\n")

totalentries = int(soup.find('totalentries').text)
print(str(totalentries) + "\n")

items = soup.find_all('item')

print(str(len(items)) + "\n")

count = 1

for item in items:
	print(str(count), ": ", item.sellerusername.string + "\n")
	count += 1