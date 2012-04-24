#!/usr/bin/env python
import httplib2
import operator
import json
from bs4 import BeautifulSoup
from config import * 
import smtplib
import string
import sys

http = httplib2.Http()
url = 'http://www.ida.liu.se/edu/ugrad/thesis/presentations.shtml'
url = 'http://www.isy.liu.se/edu/pres/'
try:
	resp, content = http.request(url)
except:
	sys.exit(1)
"b", { "class" : "lime" }

main_div =  BeautifulSoup(content).find('div', { 'id' : 'maincontent' })
table = main_div.find('table')

tr = table.findAll('tr')

for i in range(0, len(tr) , 2):
	header = tr[i].find('td').find('b').renderContents()
	header = header.split(' - ') # first element is date, second element is area
	info = tr[i + 1].find('td')
	title = info.find('b').renderContents()
	info = info.find('font').renderContents().replace('</br>', '').replace('<br/>', '').split('<br>')
	info = [x.strip() for x in info]
	date = info[2].split(', ')
	info[2] = date[1];
	date[1] = header[0];
	entry = { 'date' : date[1] + ', ' + date[0], 'location' : info[2], 'title' : title, 'author' : info[0], 'level' : info[1], 'area' : header[1] }
	print entry
