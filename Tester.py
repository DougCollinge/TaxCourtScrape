# from TCCScraper import TCCScraper
# tcc = TCCScraper()
# docket = tcc.get_hearings()

# for hearing in docket :
#     # print(repr(hearing['date']),',',repr(hearing['appellant']),',',repr(hearing['filenumber']),',',repr(hearing['language']))
#     print( hearing )

# data = tcc.get_hearing_data("2012-4043(IT)G")
# print(data)

# def progress(max,count) :
#     print( 'Progress: {}/{} '.format(count,max) )
#
# tcc.get_hearings_table(progress,limitcount=2)

import csv
oldtable = []
with open('TCCHearings2016-05-11.csv') as file :
    rdr = csv.DictReader(file)
    for row in rdr :
        oldtable.append(row)
# print( oldtable[:4] )

byfileno = {}
for row in oldtable :
    byfileno[row["File No"]] = row

print(byfileno["2015-3471(IT)APP"])
print( list(byfileno.keys()) )