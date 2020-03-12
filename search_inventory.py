import requests
from requests.auth import HTTPBasicAuth
import json
import re
import datetime

now = datetime.datetime.now()

query="project = R1S AND issuetype in (Enhancement, Story) AND status in (Assigned, Done, \"In Dev\", \"In Progress\", \"In Review\", \"In Test\", \"Security Approved\", \"Security Review\", \"To Do\", \"Backlog\") AND component = Camping AND \"Epic Link\" = R1S-6288 ORDER BY status ASC"

url = "https://recgov.atlassian.net/rest/api/3/search"

auth = HTTPBasicAuth("xxx@xxx.com", "xxx")

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

payload = json.dumps( {
  "expand": [
    "names",
    "schema",
    "operations"
  ],
  "jql": query,
  "maxResults": 1,
  "fieldsByKeys": False,
  "fields": [
    "summary",
    "status"
  ],
  "startAt": 0
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

json_data_total = json.loads(response.text)

#json array to dictionary
total = json_data_total['total']
count = 0

while (count < total):
    payload = json.dumps( {
       "expand": [
         "names",
         "schema",
         "operations"
       ],
       "jql": query,
       "maxResults": 100,
       "fieldsByKeys": False,
       "fields": [
         "summary",
         "status"
       ],
       "startAt": count
     } )

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )
    
    json_data = json.loads(response.text)
    array_length = len(json_data['issues'])
    print("array length", array_length)    
    
    for i in range(array_length):
        JIRA_summary = json_data['issues'][i]['fields']['summary']
        JIRA_key = json_data['issues'][i]['key']
        JIRA_status = json_data['issues'][i]['fields']['status']['name']

        #extract type
        try:
            Type=re.search(r'\[(.*?)\]',JIRA_summary).group(1)
        except:
            Type = "unknown"

        #extract agency
        try:
            Agency=re.search(r'\((.*?)\)',JIRA_summary).group(1)
        except:
            Agency = "unknown"

        #clean up summary
        JIRA_summary=re.sub('Camping - ', '',JIRA_summary)
        JIRA_summary=re.sub("[\(\[].*?[\)\]]", "", JIRA_summary)
        JIRA_summary=JIRA_summary.strip()

        print(JIRA_key,",",JIRA_status,",",JIRA_summary,",",Type,",",Agency)
        
        i += 1
    
    count = count + 100
