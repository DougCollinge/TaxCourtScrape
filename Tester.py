from TCCScraper import TCCScraper
tcc = TCCScraper()
# docket = tcc.get_hearings()

# for hearing in docket :
#     # print(repr(hearing['date']),',',repr(hearing['appellant']),',',repr(hearing['filenumber']),',',repr(hearing['language']))
#     print( hearing )

# data = tcc.get_hearing_data("2012-4043(IT)G")
# print(data)

def progress(max,count) :
    print( 'Progress: {}/{} '.format(count,max) )

tcc.get_hearings_table(progress,limitcount=2)