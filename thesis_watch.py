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
urls = ['http://www.ida.liu.se/edu/ugrad/thesis/presentations.shtml', 'http://www.isy.liu.se/edu/pres/']
thesis_dict = {}
for url in urls:
	try:
		resp, content = http.request(url)
	except:
		sys.exit(1)

	main_div =  BeautifulSoup(content).find('div', { 'id' : 'maincontent' })
	table = main_div.find('table')
	tr = table.findAll('tr')
	for i in range(0, len(tr) , 2):
		header = tr[i].find('td').find('b').renderContents()
		date, area = header.split(' - ') # first element is date, second element is area
		info = tr[i + 1].find('td')
		title = info.find('b').renderContents().strip()
		author, level, info = info.find('font').renderContents().replace('</br>', '').replace('<br/>', '').split('<br>')
		author = author.strip()
		level = level.strip()
		info = info.strip()
		clock, location = info.split(', ')
		entry = { 'date' : date + ', ' + clock, 'location' : location, 'title' : title, 'level' : level, 'area' : area }
		thesis_dict.update({ author : entry })

print thesis_dict
