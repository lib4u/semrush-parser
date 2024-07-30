import requests
import uuid
from fake_headers import Headers


class SemRush:

    userId = ""
    apiKey = ""
    searchItem = ""

    def __init__(self,userId,apiKey,searchItem):
      
       self.userId = userId
       self.apiKey = apiKey
       self.searchItem = searchItem
       self.endPoint = 'https://www.semrush.com/dpa/rpc'

    def getHeders(self):
        header = Headers(
            browser="chrome",  # Generate only Chrome UA
            headers=True  # generate misc headers
        )

        return header.generate()


    def getData(self,json_data):

        cookies = {
            'visit_first': '1721674555218',
            'ga_exp_c41234be21bd4796bbf8e763': '1',
            '_sm_bot': '9a7590d6486dd5c795e9b97d7e034b5790b60ecdc1ee7f9614d1b03450c2187b',
           
        }

        headers = self.getHeders()

        
        proxies = {
    'https': 'http://1z8bRM:A1ha8v@138.59.5.67:9124',
        } 
        response = requests.post(self.endPoint, cookies=cookies, headers=headers, json=json_data, proxies=proxies)

        return response.json()




    def domainOverview(self):
        statistic = dict()
        data = self.getData(json_data={
            'id': 15,
            'jsonrpc': '2.0',
            'method': 'organic.OverviewTrend',
            'params': {
                'request_id': uuid.uuid4().urn,
                'report': 'domain.overview',
                'args': {
                    'dateType': 'monthly',
                    'searchItem': self.searchItem,
                    'searchType': 'domain',
                    'dateRange': None,
                    'database': 'us',
                    'global': True,
                },
                'userId': self.userId,
                'apiKey': self.apiKey,
            },
        })
    
        try:
            for element in data['result']:
                statistic[element['date']] = element['organicTraffic']

            return statistic
        
        except Exception:
            return { "error": data}       

    

    def organicSummary(self):
        statistic = dict()
        data = self.getData(json_data={
            "id": 20,
            "jsonrpc": "2.0",
            "method": "organic.Summary",
            "params": {
            "request_id": uuid.uuid4().urn,
            "report": "domain.overview",
            "args": {
                'searchItem': self.searchItem,
                "searchType": "domain",
                "dateType": "monthly",
                "database": "us",
                "global": 'true',
                "dateFormat": "date"
            },
            'userId': self.userId,
            'apiKey': self.apiKey,
            }
        })

    
        try:
            for element in data['result']:
                statistic[element['database']] = element['organicPositions']

            return statistic
        
        except Exception:
            return { "error": data}       

        




    def backlinksSummary(self):
    
        data = self.getData(json_data={
            "id": 21,
            "jsonrpc": "2.0",
            "method": "backlinks.Summary",
            "params": {
                "request_id": uuid.uuid4().urn,
                "report": "domain.overview",
                "args": {
                "searchItem": self.searchItem,
                "searchType": "domain"
                },
                'userId': self.userId,
                'apiKey': self.apiKey,
            }
        })

     
        try:
            return data['result']
        
        except Exception:
            return { "error": data}   

  

    

