import os, requests
from models.contribution import Contribution
from models.repositories import Repository

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={limit}&page={pageNo}"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/contributors"

headers = {
    "Authorization": "Token " + os.environ.get("GITHUB_TOKEN")
}

PAGE_LIMIT = 10

def getRepos(orgName, topNRepos, topMCommiters, pageNo):
    x = max(0, min(int(topNRepos) - (pageNo - 1) * PAGE_LIMIT, PAGE_LIMIT))
    repos_json = requests.get(repo_url.format(
        organization = orgName, limit = PAGE_LIMIT, pageNo = str(pageNo)), headers=headers).json()
    if "message" in repos_json:
        return "404"     
    repos = []
    cnt = 0
    for repo in repos_json["items"]:
        if(cnt == x):
            break
        cnt = cnt + 1
        contributors = get_contributors(orgName, repo["name"], topMCommiters)
        repos.append(Repository(repo["name"], repo["html_url"],
                          repo['forks_count'], contributors))
    return repos

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

