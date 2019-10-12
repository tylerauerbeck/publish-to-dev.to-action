#import required libraries
import requests, re, os, sys, jmespath, frontmatter

# base API endpoint for dealing with articles
API_ENDPOINT = "https://dev.to/api/articles"

# required variables
PR = os.getenv('PR_LIST_FILE')
API_KEY = os.getenv('DEV_TO_TOKEN')
STATUS=0

# get_article_id allows us to find an article id by attempting to match against the title
def get_article_id(title):
    PAGE=0
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
        return False
    else:
        article_id = article_id[0]
        return article_id

# Open our file that contains all changed files in our PR
with open(PR, 'r') as files:
    # For each of these files
    for line in files.readlines():
        # Grab only the markdown files
        if re.search("^.*.md$", line):
            title = frontmatter.load(line.strip())['title']
            # Grab the file content
            with open(line.strip(),'r') as file:
                # Replace newline characters with newline literal (for body_markdown requirements) and then assemble json request
                data = file.read().replace('\n', '\\n')
                json = '{"article":{"body_markdown": "' + data + '"}}'
            headers = {'content-type': 'application/json; charset=utf-8', 'api-key': API_KEY}
            # Check to see if the article already exists
            article_id = get_article_id(title)
            # If that article exists, just update it
            if article_id:
                r = requests.put(url = API_ENDPOINT + "/" + str(article_id), data = json.encode('utf-8'), headers = headers)
                if r.status_code != 200:
                    print("Unable to publish: " + line.strip())
                    STATUS=1
                else:
                    print("Published: " + line.strip())
            # Otherwise create a new article
            else:    
                r = requests.post(url = API_ENDPOINT, data = json.encode('utf-8'), headers = headers)
                if r.status_code != 201:
                    print("Unable to publish: " + line.strip())
                    STATUS=1
                else:
                    print("Published: " + line.strip())

# If something failed along the way, fail the entire run
if STATUS != 0:
    print("There were issues publishing one or more files. Please see logs above for more details")
    sys.exit(1)
