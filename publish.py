#import required libraries
import requests, re, os, sys, jmespath, frontmatter

API_ENDPOINT = "https://dev.to/api/articles"

PR = os.getenv('PR_LIST_FILE')
API_KEY = os.getenv('DEV_TO_TOKEN')
STATUS=0
PAGE=0

with open(PR, 'r') as files:
    for line in files.readlines():
	title = frontmatter.load(line.strip())['title']
        if re.search("^.*.md$", line):
            with open(line.strip(),'r') as file:
                data = file.read().replace('\n', '\\n')
                json = '{"article":{"body_markdown": "' + data + '"}}'
            headers = {'content-type': 'application/json; charset=utf-8', 'api-key': API_KEY}
            r = requests.post(url = API_ENDPOINT, data = json.encode('utf-8'), headers = headers)
            if r.status_code != 201:
                print("This article may already exist. Attempting to update: " + title)
                r = requests.get(url = API_ENDPOINT + "/me/all?page=" + str(PAGE), headers = headers)
                article_data = r.json()
                while article_data:
                    article_id = jmespath.search('[?title == `' + title + '`].id', article_data)
                    if article_id:
                        break
                    PAGE += 1
                    r = requests.get(url = API_ENDPOINT + "/me/all?page=" + str(PAGE), headers = headers)
                    article_data = r.json()
                if not article_data:
                    print("Unable to find Article ID. There may be an issue with the article that you're attempting to publish...")
                    STATUS=1
                else:
                    article_id = article_id[0]
                    r = requests.put(url = API_ENDPOINT + "/" + str(article_id), data = json.encode('utf-8'), headers = headers)
                    if r.status_code != 200:
                        print("Unable to publish: " + line.strip())
                        STATUS=1
            else:
                print("Published: " + line.strip())

if STATUS != 0:
    print("There were issues publishing one or more files. Please see logs above for more details")
    sys.exit(1)
