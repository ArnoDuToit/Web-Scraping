# Import all the necessary libraries for this script
import datetime
import getpass

from bs4 import BeautifulSoup
import mechanize

# Setting up mechanize
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Firefox')]

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Declare a static urls
url_login = "http://slashdot.org/my/login"
url_Home = "http://slashdot.org"
url_older = "http://slashdot.org/?page="

# Declaring the older page counter
older = 0

# Main function which calls the other functions
# the main function is the start function of the script
def main():
    # Print the greeting string
    print "Please provide login information for http://slashdot.org/"
    print ""
    # Call the getCredentials function
    getCredential()

# Date input
def Timestamp():
    # Declare a test failed variable
    fail = False
    # Asking and Except the user's date that they enter
    date_text = raw_input("Date (YYYY-MM-DD): ")
    try:
        # Testing the validity of the date that was entered
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        # Print error when the date is invalid
        print ""
        print "The date is invalid, please try again!"
        # Set the failed variable to true
        fail = True

    # Check if the function failed
    if fail:
        # If Failed = True then recall this function
        timestamp()
    else:
        # If Failed = False then call the getArticle Function and pass the
        # home page url, the entered date and the older page counter into the
        # function as parameters
        getArticle(url_Home, date_text, older)

# login credentials
def getCredential():
    # Get username
    username = raw_input("Nickname: ")

    # Get password
    password = getpass.getpass('Password: ')  #password = raw_input("Password: ")

    # Test for empty Username
    if username != "":
        # If the Username is not = the an empty value
        # then test for empty Password
        if password != "":
            # If the Password is not = the an empty value
            # then print "Trying to login:"
            print ""
            print "Trying to login:"
            # Call the login function and pass the username and password into the function
            # as parameters
            login(username, password)
        else:
            # Print error string
            print "Nickname or password is invalid, please try again"
            print ""
            # Recall this function
            getCredential()
    else:
        # Print error string
        print "Nickname or password is invalid, please try again"
        print ""
        # Recall this Function
        getCredential()

# Login to the site
def login(username, password):
    # Open the login page and read the page
    openPage = br.open(url_login).read()
    # Get the response of the page
    response = br.response()

    # Get the Login form on the page
    br.form = list(br.forms())[1]
    # Enter the username into the Nickname field
    br['unickname'] = username
    # Enter the username into the Password field
    br['upasswd'] = password
    # Submit the form
    response1 = br.submit()

    # Read the response of the page
    page = response1.read()
    soup = BeautifulSoup(page)
    # Check if the page responded with any errors
    Errorslen = len(soup.findAll('div', class_="error"))

    # Test if login has failed
    if Errorslen > 0:
        # Print Error message
        print ""
        print "Nickname or password is invalid, please try again!"
        # Call the Credentials function so that the user can reenter
        # their login information
        getCredential()
    else:
        # Print successful login message
        print ""
        print "Login was successful."
        print ""
        print "Enter a timestamp to where the search should go back to:"
        # Call the timestamp function
        Timestamp()

# Try to extract the heading, author and timestamp
def getArticle(url, timestamp, oldCount):
    # Open the url that was passed in as a parameter
    html_text = br.open(url)
    # Get the HTML Page
    soup = BeautifulSoup(html_text)
    # Get all the Authors links tags (Unprocessed)
    all_Authors = soup.findAll('a',rel="nofollow")
    # Get all the articles (Unprocessed)
    all_h2 = soup.findAll('h2', class_='story')
    # Get all the time tags of all the articles (Unprocessed)
    all_dates = soup.findAll('time')

    # Declare the arrays for all the headlines
    head1 = []
    # Declare the arrays for all the authors
    author1 = []
    # Declare the arrays for all the dates
    date1 = []

    # Loop through all the articles
    for item in all_h2:
        # Append the head1 array with the article headline
        head1.append(item.find("span").find("a", href=True).get_text())

    # Loop through all the author link tags
    for author in range(1,len(all_Authors)):
        # Get all the Author links
        authors = soup.findAll('a',rel="nofollow")[author-1]
        # Loop through the links
        for x in authors:
            # Append the author1 array with the article author
            author1.append(x)

    # Loop through the time tags
    for date in range(1,len(all_dates)):
        # Get the date tags inside the time tags
        dates = soup.findAll('time')[date-1]
        # Loop through the date tags
        for x in dates:
            # Append the date1 array with the date text
            date1.append(x)

    # Declare a print counter
    countPrint = 0

    # Loop through all the articles
    for z in range(1,len(all_h2)):
        # Get the length of the date string
        sDate = date1[z-1]
        if sDate[:10] == 'on Monday ':
            # Get the following string : 'on Monday '
            day = sDate[:10]
        elif sDate[:11] == 'on Tuesday ':
            # Get the following string : 'on Tuesday '
            day = sDate[:11]
        elif sDate[:13] == 'on Wednesday ':
            # Get the following string : 'on Wednesday '
            day = sDate[:13]
        elif sDate[:12] == 'on Thursday ':
            # Get the following string : 'on Thursday '
            day = sDate[:12]
        elif sDate[:10] == 'on Friday ':
            # Get the following string : 'on Friday '
            day = sDate[:10]
        elif sDate[:10] == 'on Sunday ':
            # Get the following string : 'on Sunday '
            day = sDate[:10]
        else:
            # Get the following string : 'on Saturday '
            day = sDate[:12]

        # Declare cstring array for all the comparison strings
        cstring = ['on Monday ', 'on Tuesday ', 'on Wednesday ', 'on Thursday ', 'on Friday ', 'on Saturday ', 'on Sunday ']

        # Loop through all the comparison strings
        for y in cstring:
            # Test if article is in the date range, by calling the getDate function
            # and passing in the following in as parameters:
            # the x value, the y value the length of the x value, the length of the
            # collected date and the timestamp that the user has entered
            mayPrint = getDate(day,y,len(day),sDate, timestamp)
            # Check if the Result can be printed
            if mayPrint:
                # Increment the print counter
                countPrint += 1
                # print the result
                print ""
                print "Headline:      " + str(head1[z-1])
                print "Author:        " + str(author1[z-1])
                print "Date posted:   " + str(date1[z-1])

    #Test if how many headlines was printed
    if countPrint != 0:
        # increment the older page counter
        oldCount += 1
        # Create the full older url
        back = url_older + str(oldCount)
        # Print the link that is used to print the older articles
        print ""
        print "Going to older posts:"
        print back
        # Recall this function with the following parameters
        # The older link, the timestamp that the user has entered
        # and the older page counter
        getArticle(back, timestamp, oldCount)
    else:
        print ""
        print "No further results were found"
        # Pause the program so that the user could read through the results
        Timestamp()

# Converting the Month text into the month number
def convertMonth(month):
    val = ""
    if month == "January":
        val = "01"
    elif month == "February":
        val = "02"
    elif month == "March":
        val = "03"
    elif month == "April":
        val = "04"
    elif month == "May":
        val = "05"
    elif month == "June":
        val = "06"
    elif month == "July":
        val = "07"
    elif month == "August":
        val = "08"
    elif month == "September":
        val = "09"
    elif month == "October":
        val = "10"
    elif month == "November":
        val = "11"
    elif month == "December":
        val = "12"

    # Return the Month number
    return val

# Read and convert the site's date into a valid date
def valDate(date):
    # Get the Year
    year = date[-4:]
    # Get the Day
    day = date[-8:-6]
    # Get the month's number by calling the convertMonth
    # function with the moth text as a parameter
    month = convertMonth(date[:-9])
    # Build the date string
    vDate = year + "-" + month + "-" + day
    # Declare a failed variable
    fail = False

    try:
        # Test for a valid date
        datetime.datetime.strptime(vDate, '%Y-%m-%d')
    except:
        # Print the error string
        print ""
        print "Could not test the Date:"
        print vDate
        print ""
        print "Please try again:"
        # Set the failed variable tto True
        fail = True

    # Test if failed variable is False
    if fail != True:
        # If the failed variable is False
        # then return the date string
        return vDate
    else:
        # If the failed variable is True
        # then restart the process by recalling the timestamp function
        timestamp()

# Function that tests if the article is in the date range
def getDate(day, cDate, SliceValue, StringValue, endDate):
    # Test if the collected day from the site is equal to the coded date
    if str(day) == cDate:
        # Set tdate = the date from the sight (e.g. March 30, 2015)
        tdate = StringValue[SliceValue:-9]
        # Validate tdate and set headDate = to it
        headDate = valDate(tdate)

        # Test if the article date is after the timestamp that the user have entered
        if headDate >= endDate:
            # If it is True then return true
            return True
        elif headDate < endDate:
            # If it is before the timestamp then return return False
            return False
    else:
        return False

main()