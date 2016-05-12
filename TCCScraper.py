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
        limitcount = 0  # For debugging. Set to zero for no limit.
        hearings = []
        params = {'hearingLoc':50, 'dateRange':'all', 'form_submit':'Next'}
        r = requests.post(self.tccHearingsUrl,params)
        soup = BeautifulSoup(r.text,"html.parser")
        # print( soup.prettify() )
        tb = soup.table
        # print(tb)
        if tb != None :
            for tr in tb.find_all("tr"):
                # print(tr)
                tds = tr.find_all("td")
                # print("Len(tds):",len(tds))
                if len(tds) >= 4 :
                    # print(tds)
                    # hearings.append( {'date':week, 'appellant':tds[1].string, 'filenumber':tds[2].string, 'language':tds[3].string} )
                    hearings.append( {'Hearing Date':tds[0].string, 'Appellant Name:':tds[1].string, 'File No':tds[2].string, 'Language':tds[3].string} )
                    # hearings.append(tds[2].string)
            if limitcount != 0 :
                hearings = hearings[:limitcount]
        return hearings

    # def get_hearings(self):
    #     hearings = []
    #     weeks = self.get_weeks()
    #     for week in weeks :
    #         params = {'hearingLoc': 50, 'dateRange': week, 'form_submit':'Next'}
    #         # print(params)
    #
    #         r = requests.post(self.tccHearingsUrl, params)
    #         soup = BeautifulSoup(r.text)
    #         # print(soup.prettify())
    #         tb = soup.table
    #         # print(tb)
    #         if tb != None :
    #             for tr in tb.find_all("tr"):
    #                 # print(tr)
    #                 tds = tr.find_all("td")
    #                 # print("Len(tds):",len(tds))
    #                 if len(tds) >= 4 :
    #                     # print(tds)
    #                     # hearings.append( {'date':week, 'appellant':tds[1].string, 'filenumber':tds[2].string, 'language':tds[3].string} )
    #                     hearings.append(tds[2].string)
    #     return hearings

    def get_data_headings(self):
        return self.data_headings

    def get_hearing_data(self, file_number):
        params = {'opt':'NUMBER','t_string':file_number}
        r = requests.post(self.tccSearchUrl,params)
        soup = BeautifulSoup(r.text,"html.parser")
        data = {'File No':file_number}
        appeal_details = soup.find("table",summary="Appeal Details")

        for tr in appeal_details.children:
            # if tr.name != None:
            if tr.name == "tr":
                if tr.td and tr.th:
                    data[tr.th.string] = tr.td.string

        appellant_info = soup.find("table",summary="Appellant Information")
        if appellant_info:
            for tr in appellant_info.children:
                if tr.name == "tr":
                    data[tr.th.string] = tr.td.string

        return data

    def get_hearings_table(self,progress):
        table = self.get_hearings()
        progressmax = len(table)
        progresscount = 0
        for hearing in table:
            progresscount+=1
            progress(progressmax,progresscount)
            filenumber = hearing['File No']
            moredata = self.get_hearing_data(filenumber)
            hearing.update(moredata)
            # print(hearing)
        return table
