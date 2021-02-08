'''
	=== RUN WITH GUNICORN ===  
	* HOW TO RUN:
		- install requirements : pip3 install -r requirements.txt
		- cd <dir to root project>
		- nohup gunicorn --bind=<IP>:<PORT> --workers=2 --threads=3 read:app &
		- Number of workers and threads 
			+ Gunicorn should only need 4-12 worker processes to handle hundreds or thousands of requests per second.
			+ Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off with.
			+ Recomended: 4 CPU should be 9 workers. EX: gunicorn --workers=3 --threads=3  ...
	* HOW TO STOP:
		pkill gunicorn

	this api to read file excel file in local
	Content-Type : application/json
	method : post
	url : <ip>:<port>/read
	input : 
		- path_file : (string) path to file in local or valid link   <*.xlsx>
		- row_start : (int) row to start read
		- rows_read : (int) rows read
		- sheet_read : (int) sheet id to read (not name)
		- has_header : (int) 0 or 1 . read and append row_start to head of data
	output : 
		- status : (string) "error" : "success"
		- desc : Description error or read
		- data : data return if success 

'''

import sys
import os
import json
import xlrd
import redis
from flask_restful import Api, Resource, reqparse
import requests
from waitress import serve
#import utils
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = ROOT_DIR+'/tmp_file/'
sys.path.append(os.path.abspath(ROOT_DIR+'/utils/'))

from UtilsCheck import *
from waitress import serve
from flask import Flask, request, json,render_template

host_conf = look_ip_address()
port_conf = look_port(host_conf)

app = Flask(__name__)

@app.route('/read', methods=['POST'])
def read():
	rStatus = 'error' #error
	rDesc = 'Unknow error'
	rData = []
	rCode = 400
	try:
		parser = reqparse.RequestParser()
		parser.add_argument("path_file", type = str, trim = True)
		parser.add_argument("row_start" , type = int)
		parser.add_argument("rows_read" , type = int)
		parser.add_argument("sheet_read" , type = int)
		parser.add_argument("has_header", type = int)
		params = parser.parse_args()

		if params['path_file'] is None:
			raise Exception('path_file is required!')
		else:
			path_file = params['path_file']
			if validUrl(path_file):
				#download file tmp
				r = requests.get(path_file, allow_redirects=True)
				tmp_name = path_file.split('/')[-1]
				open(TMP_PATH+tmp_name, 'wb').write(r.content)
				path_file = TMP_PATH+tmp_name

		row_start = 0 if params['row_start'] is None else int(params['row_start'])
		sheet_read = 0 if params['sheet_read'] is None else params['sheet_read']

		book = xlrd.open_workbook(path_file)
		sheet = book.sheet_by_index(sheet_read)

		if params['rows_read'] is None or (row_start + int( params['rows_read'])) > sheet.nrows:
			rows_read = sheet.nrows
		else:
			rows_read = row_start + int( params['rows_read'])
		
		values = [sheet.row_values(i) for i in range(row_start, rows_read)]

		for value in values:
			if params['has_header'] is None:
				rData.append(value)
			else:
				if int(params['has_header']) not in [1,0]:
					raise Exception("has_header must be: 0 or 1")
				elif int(params['has_header']) == 1:
					keys = sheet.row_values(0)
					rData.append(dict(zip(keys, value)))
				else:
					rData.append(value)

		#xoá file tạm sau khi đọc xong
		if validUrl(params['path_file']):
			os.remove(TMP_PATH+tmp_name)
		
		rCode = 200
		rStatus = 'success'
		rDesc = {'status' : 'Read file success!',
				'path_file': path_file,
				'row_start' : row_start,
				'rows_read': rows_read,
				'sheet_read': sheet_read}
	except Exception as e:
		rDesc = str(e)
		rCode = 400
	finally:
		return {
			'status' : rStatus,
			'desc' : rDesc,
			'data' : rData
		}, rCode

if __name__ == '__main__':
	#Run with gunicorn
	#serve(app, host= host_conf, port=port_conf)
	#Withow Gunicorn
	app.run(host = host_conf, port = port_conf)
