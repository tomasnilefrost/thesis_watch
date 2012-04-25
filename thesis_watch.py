#!/usr/bin/env python
import httplib2
import operator
import json
from bs4 import BeautifulSoup
from config import * 
import smtplib
import string
import sys

def format_thesis(author, info):
	string = "\n"
	string += "What: " + info['title'] + "\n"
	string += "Who: " + author + "\n"
	string += "When: " + info['date'] + "\n"
	string += "Location: " + info['location'] + "\n"
	string += "Area: " + info['area'] + "\n"
	string += "Level: " + info['level'] + "\n"
	return string

old_dict = {}
try:
	f = open(config_dump_filename, 'r')
	content = f.read()
	old_dict = json.loads(content)
	f.close()
except:
	# we will simply compare with an empty dictionary of the "old" these
	pass

http = httplib2.Http()
urls = ['http://www.ida.liu.se/edu/ugrad/thesis/presentations.shtml', 'http://www.isy.liu.se/edu/pres/']
theses_dict = {}
for url in urls:
	try:
		resp, content = http.request(url)
	except:
		sys.exit(1)

	main_div =  BeautifulSoup(content).find('div', { 'id' : 'maincontent' })
	table = main_div.find('table')
	tr = table.findAll('tr')
	for i in range(0, len(tr) , 2):
		header = tr[i].find('td').find('b').renderContents().decode('utf-8')
		date, area = header.split(' - ') # first element is date, second element is area
		info = tr[i + 1].find('td')
		title = info.find('b').renderContents().strip().decode('utf-8')
		author, level, info = info.find('font').renderContents().replace('</br>', '').replace('<br/>', '').split('<br>')
		author = author.strip().decode('utf-8')
		level = level.strip().decode('utf-8')
		info = info.strip().decode('utf-8')
		clock, location = info.split(', ')
		entry = { u'date' : date + u', ' + clock, u'location' : location, u'title' : title, u'level' : level, u'area' : area }
		theses_dict.update({ author : entry })


print theses_dict
print old_dict

new_theses = [thesis for thesis in theses_dict if thesis not in old_dict]

mail_str = ""
if (len(new_theses) != 0):
	mail_str = "New theses added:\n"
	# done alphabetically
	for x in sorted(new_theses):
		mail_str += format_thesis(x, theses_dict[x])

print mail_str

# we have produced output, thus we shall mail the user and update our dump file
if (mail_str != ""):
	f = open(config_dump_filename, 'w')
	f.write(json.dumps(theses_dict))
	f.close()
	body = string.join((
			"From: %s" % config_email_from,
			"To: %s" % config_email_to,
			"Subject: %s" % config_email_subject ,
			"",
			mail_str
			), "\r\n")
	server = smtplib.SMTP(config_email_host)
	server.sendmail(config_email_from, [config_email_to], body)
	server.quit()
