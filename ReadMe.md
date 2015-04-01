# Web-scraping project
## Introduction
This document will describe what each Task does and how it works. The tools that was used to do each task is:

- Python 2.7.3
- Mechanize
- BeatifullSoup

These tools were used to fetch website pages over HTTP and parsing the resulting HTML.  In each task I tried to adhere to PEP 8 standards and I tried to build each task as readable as possible and have commented before every line of program code that explains that line.


## Task A - Aggregate news headlines
This task is a Python script that takes the Username and Password for a slashdot.org account. Mechanize and BeautifullSoup is used to log into http://slashdot.org/ through the use of the credentials the user has provided. When the login process fails then it gets handled and the user can retry logging in. So when the login process is successful then this script will ask the user to input a timestamp and then the script will then run through the page and get all the headlines, authors and timestamps.

When all the data has been collected then the data gets processed into information and then it is printed. After all the information has been printed then it will follow the older link and then the data retrieval process will start again and this will go on and on until the entered timestamp has been reached.  Once it got all the information then the script will ask the user to enter a new timestamp and so the whole process starts again.


## Task B – Find movie release dates
This task is a Python script that allows the user to search the imdb.com database for movie release dates.  This script makes use of Mechanize and BeatifullSoup to provide the search functionality and then the script searches the web site and the first 10 titles and release dates are printed.  When it is done printing the script will ask the user to search for another title.
