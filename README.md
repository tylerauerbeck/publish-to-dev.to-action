# publish-to-dev.to-action

## Disclaimer

This is a work in progress. Currently it provides initial functionality to publish a new article to the Dev.to blogging platform. Being able to update articles 

## What does this action do?

This action takes a file that provides a listing of files that you are interested in (i.e. files that were changed in a pull request, provided by a previous action or step) and then scrapes that list for markdown files. Once it has filtered for just markdown files, it then assembles an appropriate json request and sends it to Dev.to. As long as everything is successful, the action will let you know that the article has been pushed to dev.to. Otherwise it will let you know that the file has failed and it will fail that run of the action.

## Assumptions

This action assumes that you are using frontmatter in your markdown to provide a number of required fields. This was done as it seemed the easiest way to provide a number of the required fields that the api expects without having to rely on scraping and parsing information from additional files, etc. This could be re-evaluated in the future if necessary.

Frontmatter Example:
```
---
title: Hello, World!
tags: discuss, help
series: Hello series
published: false
---
This is a test
```

To see a full list of available fields for frontmatter, please look here [here](https://docs.dev.to/api/#tag/articles/paths/~1articles/post)

## Workflow Example
```
name: Publish to Dev.to
on: [pullrequest]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Publish articles 
      uses: tylerauerbeck/publish-to-dev.to-action@master
      env:
        DEV_TO_TOKEN: ${{ secrets.DEV_TO_TOKEN }}
        PR_LIST_FILE: "/github/home/pr-files"
```
## Requirements:

You'll notice that the above example relies on two environment variables: `DEV_TO_TOKEN` and `PR_LIST_FILE`. 

### DEV_TO_TOKEN
You'll need to set up an API token in your Dev.to account before you're able to configure this inside of your repo. You can find instructions on how to set up your API token [here](https://docs.dev.to/api/#section/Authentication). For instructions on how to add your secret to your repo, please check [here](https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables).

### PR_LIST_FILE
The second environment variable is the file that contains a list of files that you're interested working. As mentioned previously, you can rely on a previous step in your workflow to generate this file in a certain location (ideally in the shared filesystem that is shared between steps: `/github/home`. But this can also just be a file that is maintained within your repo if you know that you're only going to work with certain files.
