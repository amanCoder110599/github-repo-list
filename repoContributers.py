import os, requests
from models.contribution import Contribution
from models.repositories import Repository

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={limit}&page={pageNo}"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/contributors"

headers = {
    "Authorization": "Token " + os.environ.get("GITHUB_TOKEN")
}

PAGE_LIMIT = 5
page_url = "http://127.0.0.1:5000/get-repos?orgName={}&topNRepos={}&topMCommiters={}&pageNo={}"

def getRepos(orgName, topNRepos, topMCommiters, pageNo):
    x = max(0, min(int(topNRepos) - (pageNo - 1) * PAGE_LIMIT, PAGE_LIMIT))
    repos_json = requests.get(repo_url.format(
        organization = orgName, limit = PAGE_LIMIT, pageNo = str(pageNo)), headers=headers).json()
    next_page = "#"
    prev_page = "#"
    if "message" in repos_json or len(repos_json) == 0 or pageNo <= 0 or int(topNRepos) <= 0 or int(topMCommiters) < 0:
        return "404" , prev_page, next_page
    repos_json_next = requests.get(repo_url.format(
        organization = orgName, limit = PAGE_LIMIT, pageNo = str(pageNo + 1)), headers=headers).json()
    nextPageNo = pageNo + 1
    prevPageNo = pageNo - 1
    
    if(repos_json_next != 404 and x == PAGE_LIMIT):
        next_page = page_url.format(orgName, topNRepos, topMCommiters, str(nextPageNo))
    if(pageNo > 1):
        prev_page = page_url.format(orgName, topNRepos, topMCommiters, str(prevPageNo))
    repos = []
    cnt = 0
    for repo in repos_json["items"]:
        if(cnt == x):
            break
        cnt = cnt + 1
        contributors = get_contributors(orgName, repo["name"], topMCommiters)
        repos.append(Repository(repo["name"], repo["html_url"],
                          repo['forks_count'], contributors))
    return repos, prev_page, next_page

def get_contributors(orgName, repo, m):
    contributors_json = requests.get(contributors_url.format(
        organization = orgName, repo = repo), headers = headers).json()
    contributors = []
    cnt = 0
    for contributor in contributors_json:
        if(cnt == int(m)):
            break
        if(contributor["login"] == None):
            continue
        cnt = cnt + 1
        contributors.append(Contribution(contributor["login"], contributor["html_url"], contributor["contributions"]))
    return contributors

