# github-repo-list

github-repo-list is a Flask web application which finds the n most popular repositories of a given organization on Github based on the number of forks. For each such repository it also finds the top m commiters and their commit counts.

## Installation

Install all the dependencies with

```bash
   pip install -r requirements.txt
```

## Usage

1. Open the file `repoContributers.py` and paste your Github API Authentication Token in line 9.

2. Run the python file `wsgi.py` using

```bash
python wsgi.py
```

This starts the FLASK_APP in port 5000.
