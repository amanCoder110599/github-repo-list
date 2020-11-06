import os, requests
from models.contribution import Contribution
from models.repositories import Repository

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={limit}&page={page_no}"
contributors_url = "https://api.github.com/repos/{organization}/{repo}/contributors?page={page_no}"

# Add your Github API Authentication Token
token = "5b5b309e2218df7c55a2d94a8ad3c28603495d7a"

headers = {
    "Authorization": "Token " + token
}

PAGE_LIMIT = 5
PAGE_URL = "/get-repos?org_name={}&top_n_repos={}&top_m_commiters={}&page_no={}"

def getRepos(org_name, top_n_repos, top_m_commiters, page_no):
    print(org_name, top_n_repos, top_m_commiters, page_no)
    x = max(0, min(int(top_n_repos) - (page_no - 1) * PAGE_LIMIT, PAGE_LIMIT))
    repos_json = requests.get(repo_url.format(
        organization = org_name, limit = PAGE_LIMIT, page_no = str(page_no)), headers=headers).json()

    next_page = "#"
    prev_page = "#"

    if "message" in repos_json or len(repos_json) == 0 or page_no <= 0 or int(top_n_repos) <= 0 or int(top_m_commiters) < 0:
        return "404" , prev_page, next_page

    #Fetch the next page to get the details of the next page for the UI 
    repos_json_next = requests.get(repo_url.format(
        organization = org_name, limit = PAGE_LIMIT, page_no = str(page_no + 1)), headers=headers).json()
    
    nextpage_no = page_no + 1
    prevpage_no = page_no - 1
    
    if("message" in repos_json_next or x == PAGE_LIMIT):
        next_page = PAGE_URL.format(org_name, top_n_repos, top_m_commiters, str(nextpage_no))
    if(page_no > 1):
        prev_page = PAGE_URL.format(org_name, top_n_repos, top_m_commiters, str(prevpage_no))
    
    repos = []
    cnt = 0
    for repo in repos_json["items"]:
        if(cnt == x):
            break
        cnt = cnt + 1
        contributors = get_contributors(org_name, repo["name"], top_m_commiters)
        repos.append(Repository(repo["name"], repo["html_url"],
                          repo['forks_count'], contributors))

    return repos, prev_page, next_page

def get_contributors(org_name, repo, top_m_commiters):

    cnt = 0
    contributors = []
    page_no = 1

    #Since each page GET request gives only 30 contributors at a time, 
    # perform the GET request till no of contributors fetched is less than top_m_commiters
    while(cnt < int(top_m_commiters)): 
        contributors_json = requests.get(contributors_url.format(
            organization = org_name, repo = repo, page_no = str(page_no)), headers = headers).json()
        if(len(contributors_json) == 0): #If no more page available
            break   

        for contributor in contributors_json:
            if(cnt == int(top_m_commiters)):
                break
            if(contributor["login"] == None): #If contributor details does not exist
                continue
            cnt = cnt + 1
            contributors.append(Contribution(contributor["login"], contributor["html_url"], contributor["contributions"]))
        
        page_no = page_no + 1
    
    return contributors

