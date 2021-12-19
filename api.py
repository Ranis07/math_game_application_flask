#=============Requesting API from RapidApi===================

import requests

url = "https://covid-19-data.p.rapidapi.com/country/code"

querystring = {"code":"np"}

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "11f091158cmsh0c9dfafca9d0d73p13119fjsn20ae48de3d7d"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
content = response.text
confirmed = content[32:99]
lastupdate = content[184:208].upper()+'"'
# print(content)
# print(confirmed)
# print(lastupdate)