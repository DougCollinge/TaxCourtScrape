import csv
from datetime import date
from TCCScraper import TCCScraper

tcc = TCCScraper()
# docket = ['2012-4043(IT)G','2013-3987(IT)G','2015-2963(GST)I']
# docket = ['2015-4070(IT)APP']
# docket = ['2015-3296(GST)I']

def progress(max,count) :
    print( 'Progress: {}/{} '.format(count,max) )

if 'docket' not in vars():
    print("Fetching all document numbers...")
    table = tcc.get_hearings_table(progress)

fieldnames = tcc.get_data_headings()

datestr = date.today().isoformat()
filename = 'TCCHearings' + datestr + '.csv'

dial = csv.excel
dial.lineterminator = '\n'

with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=dial)
    writer.writeheader()

    print("Number of files found:",len(table))
    writer.writerows(table)
    csvfile.close()
