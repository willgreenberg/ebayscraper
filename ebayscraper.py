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
Keywords = input("Enter a search term: \n")

# Initialize the Finding api from ebaysdk with my appid
api = Finding(appid='WillGree-Scraper-PRD-d8bba853c-c16e72d4', config_file=None)

# Generate a searchRequest dictionary with all appropriate attributes (consider making this
# customizable later)
searchRequest = { 
	'keywords':Keywords,
	'outputSelector':'SellerInfo',
	'paginationInput': { 'entriesPerPage':100 }
}

# Execute the first search call to eBay
response = api.execute('findItemsByKeywords', searchRequest)

# Parse the raw HTML response, and retrieve the response object as a dictionary (might not need soup?)
responseSoup = soup(response.content, 'html.parser')
responseDict = response.dict()

# Extract all 'items' from the parsed response
items = responseSoup.find_all('item')

# Extract search information from responseDict
numTotalPages = responseDict['paginationOutput']['totalPages']
numTotalEntries = responseDict['paginationOutput']['totalEntries']
currPage = responseDict['paginationOutput']['pageNumber']

# DEBUG - print search information
print("Number of Total Pages to Search: " + str(numTotalPages))
print("Number of Total Entries: " + str(numTotalEntries))
print("Current Page: " + str(currPage))

# Loop over subsequent pages in the search, 100 entries per page
for page in numTotalPages:
	response = api.next_page()
	responseSoup = soup(response.content, 'html.parser')
	responseDict = response.dict()
	newItems = responseSoup.find_all('item')
	items += newItems

	currPage = responseDict['paginationOutput']['pageNumber']
	print("Current Page: " + str(currPage))


# DEBUG
# print(soup.text + "\n")
# totalentries = int(soup.find('totalentries').text)
# print(str(totalentries) + "\n")

# # DEBUG
print("Number of items: " + str(len(items)))

# DEBUG - list out item information
count = 1
for item in items:
	print(str(count), ": ", item.title.string)
	count += 1





