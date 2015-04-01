# Import all the necessary libraries for this script
import urllib
import urllib2
import cookielib
import urlparse
from bs4 import BeautifulSoup
import mechanize

# Setting up mechanize
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent','Firefox')]

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Declare a static urls
url_SearchP1 = "http://www.imdb.com/find?ref_=nv_sr_fn&q="
url_SearchP2 = "&s=all"
url_Home = "http://www.imdb.com"

count = 0

# Initialise the script
def main():
    counter = 0
    count = counter
    # Print a greeting message
    print "Enter the name of the Titles you want to search for: "
    # Call the searchTitle function
    searchTitle()

# This is the search function
def searchTitle():
    # Get user input
    searchItem = getSearchLink(raw_input("Search for: "))
    # Print a busy message for the user
    print ""
    print "Searching for the title"
    print ""
    # Call the getSearchResult function to get the search results
    getSearchResults(searchItem)

# This function creates the search link
def getSearchLink(searchItem):
    # Declare a variable to save the new search item
    item = ""

    # Loop through all the characters in searchItem
    for x in range(0,len(searchItem)):
        # Get the character at the current position
        char = searchItem[x:x+1]
        # Test if the character is a space or not
        if char == " ":
            # Replace the space with a '+' sign
            item = item + "+"
        else:
            # Just return the character
            item = item + char

    # Compile the search
    item = url_SearchP1 + item + url_SearchP2
    # Return the link
    return  item

# This function gets the search results
def getSearchResults(url):
    # Create a list of titles
    titles = []
    try:
        # Opening the search link
        openPage = browser.open(url)
        soup = BeautifulSoup(openPage)
        # Get the 'td' tags
        all_titles = soup.findAll('td', class_="result_text")

        # Loop through all the 'td' tags that were found
        for title in all_titles:
            # Get all the links that is within the 'td' tags
            titles.append(title.find("a", href=True))
    except:
        # Print error message
        print ""
        print "No results fount please try again"
        # Recall the search function so that the user can search for another title
        searchTitle()

    # Test if any titles were fount
    if len(titles) != 0:
        counts = count
        # Loop through the list of titles
        for title in titles:
            if counts <= 10:
                counts = counts + 1
                title['href'] = urlparse.urljoin(url_Home, title['href'])
                # Print each title
                getTitleInfo(title['href'], counts)

    print "Above is all the search results:"
    main()

# This function gets prints the titles and release dates
def getTitleInfo(url, count):
    # Declare 2 arrays
    itemTitle = []
    RelDate = []
    # Declare failed variable for testing purposes
    failed = False

    try:
        # Open the url
        openPage = browser.open(url)
        soup = BeautifulSoup(openPage)
        # Get all the "h1" tags that belongs to the 'header' class
        titles = soup.findAll('h1', class_="header")
        # Get all the 'div' tags that belongs to the 'infobar' class
        nav = soup.findAll('div', class_="infobar")

        # Loop through all the 'div' tags that belongs to the infobar class
        for date in nav:
            # Add the release date to the array
            RelDate.append(date.find("a", title="See all release dates").getText())

        # Loop through all the "h1" tags that belongs to the 'header' class
        for item in titles:
            # Add the title to the array
            itemTitle.append(item.find("span", class_="itemprop").getText())
    except:
        # Set failed to True when something went wrong
        failed = True

    # Test if Failed stayed False
    if failed == False:
        # Print the result
        # Loop through all the items in the Title array
        for x in range(0,len(itemTitle)):

            print "Result: " + str(count)
            print "Title: " + itemTitle[x]
            print "Release Date: " + RelDate[x]
            print ""

main()