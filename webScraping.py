from urllib.request import urlopen
from urllib.error   import HTTPError
from bs4            import BeautifulSoup

def getTitle(url):
   try:
      html = urlopen(url)
   except HTTPError as e:
      return None
   try:
      bso = BeautifulSoup(html.read())
      title = bso.findAll("h1")
   except AttributeError as e:
      return None
   return title

url = "http://pythonscraping.com/pages/page1.html"
titles = getTitle(url)
for title in titles:
   print(title.get_text())
