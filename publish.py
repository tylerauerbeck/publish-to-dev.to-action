#import required libraries
import requests, re, os, sys

API_ENDPOINT = "https://dev.to/api/articles"

PR = os.getenv('PR_LIST_FILE')
API_KEY = os.getenv('DEV_TO_TOKEN')
STATUS=0

with open(PR, 'r') as files:
    for line in files.readlines():
        if re.search("^.*.md$", line):
            with open(line.strip(),'r') as file:
                data = file.read().replace('\n', '\\n')
                json = '{"article":{"body_markdown": "' + data + '"}}'
            headers = {'content-type': 'application/json; charset=utf-8', 'api-key': API_KEY}
            r = requests.post(url = API_ENDPOINT, data = json.encode('utf-8'), headers = headers)
            if r.status_code != 201:
                print("Unable to publish: " + line.strip())
                STATUS=1
            else:
                print("Published: " + line.strip())

if STATUS != 0:
    print("There were issues publishing one or more files. Please see logs above for more details")
    sys.exit(1)
