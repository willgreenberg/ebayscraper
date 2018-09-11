# eBay Scraper
# By Will Greenberg
# July 17, 2018

# Purpose: Given an eBay search term, compile a list of all items with information on bid price, 
# Buy-It-Now option, time left, etc to be used for an AI system later

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import html.parser

# INPUTS
	# Get keywords to search with from user (or hard-coded for testing)
Keywords = input("Enter a search term: ")

	# Get the type of search the user would like
outputSelection = input("Would you like \n (a) a list of items or \n (b) an aspect histogram? ")
if outputSelection is "a":
	outputSelection = "SellerInfo"
if outputSelection is "b":
	outputSelection = "AspectHistogram"

# Initialize the Finding api from ebaysdk with my appid
api = Finding(appid='[ADD YOUR OWN]', config_file=None)

# Generate a searchRequest dictionary with all appropriate attributes (consider making this
# customizable later)
searchRequest = { 
	'keywords':Keywords,
	'outputSelector':outputSelection,
	'paginationInput': { 'entriesPerPage':100 },
	# 'itemFilter': { 'HideDuplicateItems':True }
}

try:
	# Execute the first search call to eBay
	response = api.execute('findItemsByKeywords', searchRequest)
except ConnectionError as e:
	print(e)

# Parse the raw HTML response, and retrieve the response object as a dictionary (might not need soup?)
responseSoup = soup(response.content, 'html.parser')
responseDict = response.dict()

# Extract all 'items' from the parsed response
items = responseSoup.find_all('item')

aspects = responseSoup.find_all('aspect')

# Extract search information from responseDict
numTotalPages = responseDict['paginationOutput']['totalPages']
numTotalEntries = responseDict['paginationOutput']['totalEntries']
currPage = responseDict['paginationOutput']['pageNumber']

# DEBUG - print search information
print("Number of Total Pages to Search: " + numTotalPages)
print("Number of Total Entries: " + numTotalEntries)
print("Current Page: " + str(currPage))

# Loop over subsequent pages in the search, 100 entries per page, up to 10 pages
pageNum = 1
while pageNum < 1 and pageNum < int(numTotalPages):
	try:
		response = api.next_page()
		responseSoup = soup(response.content, 'html.parser')
		responseDict = response.dict()
		newItems = responseSoup.find_all('item')
		items += newItems

		currPage = responseDict['paginationOutput']['pageNumber']
		print("Current Page: " + str(currPage))
		pageNum += 1
	except ConnectionError as e:
		print(e)

# DEBUG
# print(soup.text + "\n")
# totalentries = int(soup.find('totalentries').text)
# print(str(totalentries) + "\n")

# DEBUG
print("Number of items: " + str(len(items)))

# ASPECTS PRINT
print("\n" + "NUMBER OF ASPECTS:" + str(len(aspects)) + "\n")

count = 0
for aspect in aspects:
	print("TYPE: " + aspect['name'])
	valuehistograms = aspect.find_all('valuehistogram')
	print("VALUES:")
	for valuename in valuehistograms:
		print(" " + valuename['valuename'])
	count += 1
	print()

# ITEM INFO PRINT
if outputSelection is "SellerInfo":
	count = 1
	for item in items:

		print(str(count), ": ", item.title.string)
		print("Price: $" + item.currentprice.string, sep='')
		print("Seller: " + item.sellerusername.text)
		print("Listing Type: " + item.listingtype.string)
		print("url: " + item.viewitemurl.string, "\n")
		# print("Condition:" + item.conditiondisplayname.string)
		count += 1





