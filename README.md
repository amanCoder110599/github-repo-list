# github-repo-list

github-repo-list is a Flask web application which finds the n most popular repositories of a given organization on Github based on the number of forks. For each such repository it also finds the top m commiters and their commit counts.

## Installation

Install all the dependencies with

```bash
   pip3 install -r requirements.txt
```

## Usage

1. Open the file `repoContributers.py` and paste your Github API Authentication Token in line 9.

2. Run the python file `wsgi.py` using
   ```bash
   python3 wsgi.py
   ```

This starts the FLASK_APP in port 5000.

A couple of screenshots after the testing of the webapp

![alt text](https://github.com/amanCoder110599/github-repo-list/blob/main/Screenshot%20from%202020-11-06%2014-38-58.png)

![alt text](https://github.com/amanCoder110599/github-repo-list/blob/main/Screenshot%20from%202020-11-06%2014-39-08.png)
