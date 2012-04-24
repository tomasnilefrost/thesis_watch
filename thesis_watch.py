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
try:
	resp, content = http.request(url)
except:
	sys.exit(1)
"b", { "class" : "lime" }

main_div =  BeautifulSoup(content).find('div', { 'id' : 'maincontent' })
table = main_div.find('table')

tr = table.findAll('tr')

for i in range(0, len(tr) , 2):
	area = tr[i].find('td').find('b').renderContents()
	info = tr[i + 1].find('td')
	title = info.find('b').renderContents()
	info = info.find('font').renderContents()
	info = info.replace('</br>', '').replace('<br/>', '');
	print info
