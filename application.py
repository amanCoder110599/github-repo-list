from flask import Flask, render_template, url_for, request, redirect, jsonify
from repoContributers import getRepos


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get-repos', methods=['GET'])
def getList():
    orgName = request.args.get('orgName')
    topNRepos = request.args.get('topNRepos')
    topMCommiters = request.args.get('topMCommiters')
    pageNo = int(request.args.get('pageNo', '1'))
    repos, prevPage, nextPage = getRepos(orgName, topNRepos, topMCommiters, pageNo)
    if(repos == "404"):   
        return 'No repositories available'
    return render_template('get-repos.html', repos = repos, organization = orgName.upper(), prevPage = prevPage, nextPage = nextPage)

if __name__ == "__main__":
    app.run()
