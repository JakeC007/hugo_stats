"""
Jake Chanenson
3/9/2021
Webscraper for Hugo Award Data 
"""
from bs4 import BeautifulSoup
import urllib.request
import os.path
import csv
from collections import defaultdict
import time
import re

# Global Vars
UNIQUE_AUTH = set()
WHITELST = ["Best Novel","Best Novella", "Best Novelette", "Best Short Story"]

def main():
  # foo = grabAwardYear(2020)
  # exportToCSV(foo, "test.csv", flag = True)
  foo = grabAwardYear(1999)
  exportToCSV(foo, "test.csv", flag = True)

  for i in range(2000,2021):
    foo = grabAwardYear(i)
    exportToCSV(foo, "test.csv")

  
  
  # unqiueAuthToCSV("auth.csv")
  #TODO
  # fix regex issue 
  # create rel path stuct for cache and csv file 
  # fix the author CSV 
  # - something is off with how many authors are added to the set and the whitelist..

  # print("The 2019 Year")
  # grabAwardYear(2019)


def getpage(url, cache_file=None):

    if cache_file is not None and os.path.exists(cache_file):
        #print("Reading cache")
        cache = open(cache_file, 'r')
        page = cache.read()
        return page

    req = urllib.request.Request(url, headers={"User-Agent": "Chrome"})
    res = urllib.request.urlopen(req)
    page = res.read().decode('utf-8')

    if cache_file is not None:
        #print("Writing cache")
        cache = open(cache_file, 'w')
        cache.write(page)
        cache.close()
    
    return page

def grabAwardYear(year):
  """
  Grabs relevant content from Hugo Awrads Website
  @param:
    * year - int of which year to pull for hugo award data 
  @returns:
    * retDicts - list of dicts of all data for award year. Each element in lst is a different catagory
  """
  url = "http://www.thehugoawards.org/hugo-history/" + str(year) + "-hugo-awards/"
  cFile = str(year)+'.html'
  page = getpage(url,cache_file=cFile)
  soup = BeautifulSoup(page)

  nomData = [] # just the nominees
  retDicts = [] # list of dicts of all data for award year  

  results = soup.find_all("li", {"class":"winner"})
  for winner in results:
      category = winner.find_previous('strong')
      #process category 
      cat = category.text
      if cat not in WHITELST:
        print(f"{cat} not in whitelist. Scraping Skipped \n")
        continue
      
      print(f"** {category.text} **")

      #process winner
      print(f"WINNER {winner.text}")
      winData = winner.text
      
      all_nominees = winner.findPrevious().find_all('li')
      
      for i in range(1, len(all_nominees)):
          nomData.append(all_nominees[i].text)
          print(f"NOMINATED {all_nominees[i].text}") 
      
      bar = textProcess(year, cat, winData, nomData)

      retDicts.append(bar)
      nomData = []
      print()

  return retDicts


def textProcess(year, cat, winData, nomData):
  """
  Take the scraped data of one catagory and pack it into a dict.
  @params:
    * year - int of the award year 
    * cat - str of the award catagory
    * winData - str of the winner of the catagory
    * nomData - lst of strs of the nominees
  @returns:
    * TBD 
  """
  # set up varaibles 
  tempDict = defaultdict(list)
  pronouns = "U" # to be handled by hand at a later time

  # hanlde winner
  win_bool = "TRUE"
  title, author = cleanEntry(winData)
  tempDict[title] = [author, pronouns, cat, year, win_bool]
  

  #hanlde nominees
  win_bool = "FALSE"
  for nominee in nomData:
    #for years with no award skip the no award bullet point
    if nominee == "No Award":
      continue
    title, author = cleanEntry(nominee)
    tempDict[title] = [author, pronouns, cat, year, win_bool]

  return tempDict 

def cleanEntry(text):
  """
  Use REGEX to grab the title and author from the nomination string
  @param:
    * test - the full text of the nomination string
  @returns: 
    * title - title of book string 
    * author - author of book string
  """
  # set varaibles
  title = ""
  author = ""
 
  try:
    title = re.search('(.*),? by (.*) \W', text).group(1)
    author = re.search('(.*),? by (.*) \W', text).group(2)
  except:
    try:
      title = re.search('(.*), by (.*)', text).group(1)
      author = title = re.search('(.*), by (.*)', text).group(2)
      print("I AM USEFUL")
      time.sleep(10)
    except:
      try:
        title = re.search('(.*),? (.*) \W', text).group(1)
        author = re.search('(.*),? (.*) \W', text).group(2)
      except AttributeError:
        print(f"\nThe string is {text}\n Author: {author}\n Title: {title}\n")
        time.sleep(10)
        #TODO FIX REGEX THIS
        pass
  
  #temp fix since regex isn't perfect on grabbing the first '(' or '['
  try:
    author, junk = author.split("[")
    print(author)
  except:
    try:
        author, junk = author.split("(")
        print(author)
    except:
      print("passed")
      pass
  
  UNIQUE_AUTH.add(author.strip('"“”″')) #global var 
  
  return title.strip('“”″"'), author.strip('"“”″')

def exportToCSV(dictLst, fileName, flag = False):
  """
	Appends a given dict to the CSV file
	@params:
		* awardDict - the dict containing all Hugo awards for a given year
		* fileName - the name of the csv file 
		* flag - optional, set to TRUE if you are creating the file 
	@returns: None
	"""
  csvCol = ["Title", "Author", "Pronouns", "Category", "Year", "Winner_Bool"]
  with open(fileName, 'a') as csvFP:
    dictWriter = csv.writer(csvFP, delimiter=',')
    
    #write header if the file is new
    if flag == True:
      dictWriter.writerow(csvCol)
    
    # walk through list of dicts and write the contents
    for d in dictLst:
      for title, data in d.items():
        data.insert(0, title) #make the key (title) to the first element in the row
        dictWriter.writerow(data)
  
  return None

def unqiueAuthToCSV(auth_file):
  """
  Writes the unqiue set of authors to CSV. Needed to fill in pronouns by hand.
  @params:
    * auth_file - csv file
  @returns:
    * None 
  """
  #handle prexisiting file
  if auth_file is not None and os.path.exists(auth_file):
    authAppendHelper(auth_file)
    return None
  
  #handle no file
  if auth_file is not None:
    with open(auth_file, 'a') as csvFP:
      dictWriter = csv.writer(csvFP, delimiter=',')
      dictWriter.writerow(["Author", "Pronouns"])
      for author in UNIQUE_AUTH:
        dictWriter.writerow([author, ""])
  
  return None

def authAppendHelper(auth_file):
  """
  Helper function for unqiueAuthToCSV(). Reads in existing CSV and finds the difference between CSV author list and webscraped author list
  @params:
    * auth_file - csv file
  @returns:
    * None 
  """
  oldAuth = set()
  # read in existing CSV and create set of existing authors
  with open(auth_file, 'r') as csvFP:
    csv_reader = csv.reader(csvFP, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
            line_count += 1
        else:
          oldAuth.add(row[0])
          line_count += 1

  #get the difference between sets
  setDiff = UNIQUE_AUTH.difference(oldAuth)
  print(f"Old {oldAuth}\n\n New: {UNIQUE_AUTH}")
  print(setDiff)

  # add new authors not already in set
  with open(auth_file, 'a') as csvFP:
    csv_writer = csv.writer(csvFP, delimiter=',')
    for author in setDiff:
      csv_writer.writerow([author, ""])
  
  return None







main() 



