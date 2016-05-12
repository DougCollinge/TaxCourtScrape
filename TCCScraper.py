import requests
from bs4 import BeautifulSoup


class TCCScraper :
    def __init__(self):
        self.tccHearingsUrl = "http://cas-cdc-www02.cas-satj.gc.ca/tcc_hearings/hearings_schedule_e.php"
        self.tccSearchUrl = "http://cas-cdc-www02.cas-satj.gc.ca/tcc_docket/search_e.php"
        self.data_headings = fieldnames = [
            'Hearing Date',
            'File No', 'Act', 'Language', 'Date Filed', 'Hearing Location',
            'Procedure', 'Nature', 'Disposition', 'Status',
            'Appellant Name:','Representative Type:', 'Representative Information:'
        ]

    def get_weeks(self):
        r = requests.get(self.tccHearingsUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        options = soup.find(id='dateRange').find_all("option")
        weeks = []
        for opt in options:
            date = opt['value']
            if date != "all" and date != "":
                weeks.append(date)

        return weeks

    def get_hearings(self):
        hearings = []
        params = {'hearingLoc':50, 'dateRange':'all', 'form_submit':'Next'}
        r = requests.post(self.tccHearingsUrl,params)
        soup = BeautifulSoup(r.text,"html.parser")
        tb = soup.table
        if tb != None :
            for tr in tb.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 4 :
                    hearings.append( {'Hearing Date':tds[0].string, 'Appellant Name:':tds[1].string, 'File No':tds[2].string, 'Language':tds[3].string} )
        return hearings


    def get_data_headings(self):
        return self.data_headings

    def get_hearing_data(self, file_number):
        params = {'opt':'NUMBER','t_string':file_number}
        r = requests.post(self.tccSearchUrl,params)
        soup = BeautifulSoup(r.text,"html.parser")
        data = {'File No':file_number}
        appeal_details = soup.find("table",summary="Appeal Details")

        for tr in appeal_details.children:
            if tr.name == "tr":
                if tr.td and tr.th:
                    data[tr.th.string] = tr.td.string

        appellant_info = soup.find("table",summary="Appellant Information")
        if appellant_info:
            for tr in appellant_info.children:
                if tr.name == "tr":
                    data[tr.th.string] = tr.td.string

        return data

    def get_hearings_table(self,progress=None,limitcount=0):
        table = self.get_hearings()
        if limitcount != 0:
            table = table[:limitcount]

        progressmax = len(table)
        progresscount = 0
        for hearing in table:
            progresscount+=1
            if progress is not None :
                progress(progressmax,progresscount)
            filenumber = hearing['File No']
            moredata = self.get_hearing_data(filenumber)
            hearing.update(moredata)
        return table
