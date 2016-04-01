import requests
import csv

from TCCScraper import TCCScraper
tcc = TCCScraper()
# docket = ['2012-4043(IT)G','2013-3987(IT)G','2015-2963(GST)I']
# docket = ['2015-4070(IT)APP']
# docket = ['2015-3296(GST)I']

if 'docket' not in vars():
    print("Fetching all document numbers...")
    docket = tcc.get_hearings()

fieldnames = tcc.get_data_headings()

with open('TCCHearings.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    counter = 1
    print("File numbers found:",len(docket))
    for file_number in docket :
        print(counter,". Fetching data for file number:",file_number)
        counter += 1
        hearing_data = tcc.get_hearing_data(file_number)
        writer.writerow(hearing_data)

    csvfile.close()
