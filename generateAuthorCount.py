import xlrd
wb = xlrd.open_workbook("hugo_data.xlsx") 
 
mDict = {}
fDict = {}
nbDict = {}
for j in range(3):
  sheet = wb.sheet_by_index(j)
  for i in range(1,sheet.nrows):
    nameT, gender, title, year, junk = sheet.row_values(i)
    name=str(nameT.strip('\xa0'))
    if(gender == "F"):
      fDict[name]= fDict.setdefault(name, 0) + 1
    elif(gender == "M"):
      mDict[name]= mDict.setdefault(name, 0) + 1
    else:
      nbDict[name]= nbDict.setdefault(name, 0) + 1


print("There are %d people with she/her pronouns" % len(fDict))
print(sorted(fDict.items(), key=lambda x: x[1]))

print("\nThere are %d people with he/him pronouns" % len(mDict))
print(sorted(mDict.items(), key=lambda x: x[1]))

print("\n There are %d unqiue people with they/them pronouns" %len(nbDict))
print(sorted(nbDict.items(), key=lambda x: x[1]))
