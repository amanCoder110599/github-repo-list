from flask import Flask, render_template, request
from repoContributers import getRepos


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get-repos", methods=["GET"])
def getList():
    org_name = request.args.get("org_name")
    top_n_repos = request.args.get("top_n_repos")
    top_m_commiters = request.args.get("top_m_commiters")
    page_no = int(request.args.get("page_no", "1"))
    try:
        repos, prevPage, nextPage = getRepos(
            org_name, top_n_repos, top_m_commiters, page_no
        )
        if repos == "404" or len(repos) == 0:
            return "No repositories available"
        return render_template(
            "get-repos.html",
            repos=repos,
            organization=org_name.upper(),
            prevPage=prevPage,
            nextPage=nextPage,
        )
    except:
        return "Please enter correct parameters"
