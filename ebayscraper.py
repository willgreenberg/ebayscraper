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


# Get keywords to search with from user (or hard-coded for testing)
Keywords = 'pan' #input("Enter a search term: \n")

# Initialize the Finding api from ebaysdk with my appid
api = Finding(appid='WillGree-Scraper-PRD-d8bba853c-c16e72d4', config_file=None)

# Generate a searchRequest dictionary with all appropriate attributes (consider making this
# customizable later)
searchRequest = { 
	'keywords':Keywords,
	'outputSelector':'SellerInfo',
	'paginationInput': [ { 'entriesPerPage':100 } ]
}

# Execute the search call to eBay
response = api.execute('findItemsByKeywords', searchRequest)

# Parse the raw HTML response
soup = soup(response.content, 'html.parser')

# DEBUG
#print(soup.text + "\n")
#totalentries = int(soup.find('totalentries').text)
#print(str(totalentries) + "\n")

# Extract all 'items' from the parsed response
items = soup.find_all('item')

# DEBUG
print("Number of items: " + str(len(items)))

# DEBUG - list out item information
count = 1
for item in items:
	print(str(count), ": ", item.sellerusername.string)
	count += 1