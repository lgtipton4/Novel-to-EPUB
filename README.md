**Novel to EPUB**

Packs novels on RoyalRoad (https://www.royalroad.com/home) into the EPUB file format for offline reading on mobile devices.

What is RoyalRoad?

RoyalRoad is a platform where novice and experienced authors alike self-publish novels. The site garners over 15 millions views per month and some authors go on to officially publish their works.  

**HOW TO USE:**

Download the executable (.exe) and follow on screen instructions (enter novel name or URL).

OR

Make sure you have the following dependencies installed:
1) BeautifulSoup (pip install beautifulsoup4)
2) ebooklib (pip install EbookLib)
3) validators (pip install validators)
4) Requests (pip install requests)
5) google-auth/api libraries (IF you want to use the Kindle Email function)
To install them all: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4 EbookLib validators requests

The compiled EPUB file will be outputted in the same directory.

**For reading on Windows:**

Use an online epub reader like Flow (https://www.flowoss.com/) or read on Calibre. 

**For reading on Kindle:**

Use the built in email function to send the packed EPUB file to your Kindle. This does require some initial set-up, however. Follow this article (https://developers.google.com/gmail/api/quickstart/python) until the "Configure the Sample" stage. Add your email as a user by going to APIs & Services -> OAuth consent screen -> Audience -> Add test user. Open novel2epub and grant access to the program. 

Enable Amazon Send to Kindle (https://www.amazon.com/gp/sendtokindle/). 

Ideally, the next release will not require these steps. 

OR

Download Calibre (https://calibre-ebook.com/download) on Windows and convert the output EPUB file to MOBI. You can send the converted MOBI file to your Kindle with Calibre. 

**For reading on iPhones:**

Copy the EPUB file over to your phone via iTunes or a cloud sharing platform like DropBox, locate the EPUB in the "Files" app, and tap on it to read in the Books app. 

As an alternative to the books app, there are many EPUB readers on the AppStore. To send the EPUB file to an alternative app, locate the EPUB in the "Files" app, tap "Share" and choose the app you wish to read on.  


