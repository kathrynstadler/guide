# project-b-24

CS 3240 UVA Guide Project

## Install directions for contributers

After following the below instructions, you can install dependencies after every git pull by running

```zsh
python3 -m pip install -r requirements.txt
```

macOS: go ahead and install Homebrew if you have not by running this command in terminal:

```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Docs for Homebrew: <https://brew.sh>

- Clone repo to your desired location on your local machine
- run ```cd project-b-24```
- create virtual env by doing the following
  - Assuming you have recent Python, if not:
    - macOS:
      - ```brew install python```
    - Ubuntu: already installed, upgrade with:
      - ```sudo apt-get update && sudo apt-get upgrade```
    - Windows: download from python website
  - Set up the virtual environment in the **project-b-24** directory.
    - ```python -m venv ./env --upgrade-deps```
  - activate venv
    - Unix/macOS: ``` source env/bin/activate ```
    - Windows: ```.\env\Scripts\activate```
- Upgrade/Install **pip** for venv
  - Install: ```python -m ensurepip```
  - Upgrade: ```python -m ensurepip --upgrade```
- Install postgreSQL
  - > If you do not, you will get an error message during **pip install**. If you don't want to install postgreSQL locally, edit the requirements.txt file to not include psycopg2==2.X.X
  - macOS: ``` brew install postgresql ```
  - Ubuntu:```sudo apt install postgresql postgresql-contrib```
  - Windows: download from postgreSQL website
- Run the following command to install all requirements to you venv
  - ```python3 -m pip install -r requirements.txt```

When this is finished you should have the following results from commands (with respect to your file paths).

macOS/Unix:

```zsh
❯ python -V
Python 3.9.7

❯ which python
/Users/tapp/Documents/UVA/CS3240/project-b-24/env/bin/python

❯ python -m pip --version
pip 21.2.4 from /Users/tapp/Documents/UVA/CS3240/project-b-24/env/lib/python3.9/site-packages/pip (python 3.9)

❯ pip list
Package             Version
------------------- ---------
asgiref             3.4.1
beautifulsoup4      4.10.0
certifi             2021.5.30
charset-normalizer  2.0.6
dj-database-url     0.5.0
Django              3.2.7
django-bootstrap-v5 1.0.5
django-heroku       0.3.1
gunicorn            20.1.0
idna                3.2
importlib-metadata  3.10.1
pip                 21.2.4
psycopg2            2.8.6
python-dateutil     1.5
pytz                2021.1
requests            2.26.0
setuptools          58.2.0
soupsieve           2.2.1
sqlparse            0.4.2
urllib3             1.26.7
whitenoise          5.3.0
zipp                3.5.0
```

Windows:

```
> py -3 -V
Python 3.9.7

> where python
...\env\Scripts\python.exe

> pip3 list
charset-normalizer==2.0.6
dj-database-url==0.5.0
Django==3.2.7
django-bootstrap-v5==1.0.5
gunicorn==20.1.0
django-heroku==0.3.1
idna==3.2
importlib-metadata==3.10.1
psycopg2==2.8.6
python-dateutil==1.5
pytz==2021.1
requests==2.26.0
soupsieve==2.2.1
sqlparse==0.4.2
urllib3==1.26.7
zipp==3.5.0
```
