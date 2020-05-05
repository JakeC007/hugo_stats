import xlrd
import csv
wb = xlrd.open_workbook("hugo_data.xlsx") 

#create dicts for 3 pronoun types found in data
mDict = {}
fDict = {}
nbDict = {}
#loop through the three sheets 
for j in range(3):
  sheet = wb.sheet_by_index(j)
  #create a key for each author and incr the value each time the author is nominated 
  for i in range(1,sheet.nrows):
    nameT, gender, title, year, junk = sheet.row_values(i)
    name=str(nameT.strip('\xa0'))
    if(gender == "F"):
      fDict[name]= fDict.setdefault(name, 0) + 1
    elif(gender == "M"):
      mDict[name]= mDict.setdefault(name, 0) + 1
    else:
      nbDict[name]= nbDict.setdefault(name, 0) + 1

#write info to csv file
with open('auth_stats.csv', mode='w') as auth_file:
    auth_writer = csv.writer(auth_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    auth_writer.writerow(['Name', 'Nominations', 'Pronouns', 'Freq']) #header row
    
    for entry in fDict.items():
      auth_writer.writerow([entry[0], entry[1], 'She/Her', 1])
    
    for entry in mDict.items():
      auth_writer.writerow([entry[0], entry[1], 'He/Him', 1])
    
    for entry in nbDict.items():
      auth_writer.writerow([entry[0], entry[1], 'They/Them', 1])
  


#print sorted findings
print("There are %d people with she/her pronouns" % len(fDict))
print(sorted(fDict.items(), key=lambda x: x[1]))

print("\nThere are %d people with he/him pronouns" % len(mDict))
print(sorted(mDict.items(), key=lambda x: x[1]))

print("\n There are %d unqiue people with they/them pronouns" %len(nbDict))
print(sorted(nbDict.items(), key=lambda x: x[1]))
