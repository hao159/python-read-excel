# API READ FILE EXCEL WITH PYTHON
API read file excel(xlsx) with python.

## Requirements
  - Flask==1.1.2
  - Flask-RESTful==0.3.8
  - gunicorn==20.0.4
  - netifaces==0.10.9
  - requests==2.25.1
  - sockets==1.0.0
  - urllib3==1.26.3
  - waitress==1.4.4
  - xlrd==2.0.1

## Install requirements
  - pip3 install -r requirements.txt

## Run
  - For test:
    - python3 <path file>
  - Run single thread:
    - nohup python3 <path file> &
  - Run with gunicorn:
    - nohup gunicorn --bind=0.0.0.0:8080 --workers=2 --threads=2 app:app



