from TCCScraper import TCCScraper
tcc = TCCScraper()
# docket = tcc.get_hearings()

# for hearing in docket :
#     # print(repr(hearing['date']),',',repr(hearing['appellant']),',',repr(hearing['filenumber']),',',repr(hearing['language']))
#     print( hearing )

# data = tcc.get_hearing_data("2012-4043(IT)G")
# print(data)

tcc.get_hearings_table()