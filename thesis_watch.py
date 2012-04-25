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
	string = u"\n"
	string += u"What: " + info['title'] + u"\n"
	string += u"Who: " + author + u"\n"
	string += u"When: " + info['date'] + u"\n"
	string += u"Location: " + info['location'] + u"\n"
	string += u"Area: " + info['area'] + u"\n"
	string += u"Level: " + info['level'] + u"\n"
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


new_theses = [thesis for thesis in theses_dict if thesis not in old_dict]
something_removed = any([True for thesis in old_dict if thesis not in theses_dict])

mail_str = ""
if (len(new_theses) != 0):
	mail_str = "New theses added:\n"
	# done alphabetically
	for x in sorted(new_theses):
		mail_str += format_thesis(x, theses_dict[x])

# we have produced output, thus we shall mail the user and update our dump file
if (mail_str != ""):
	body = string.join((
			u"From: %s" % config_email_from,
			u"To: %s" % config_email_to,
			u"Subject: %s" % config_email_subject ,
			u"",
			mail_str
			), u"\r\n")
	server = smtplib.SMTP(config_email_host)
	server.sendmail(config_email_from, [config_email_to], body.encode('utf-8'))
	server.quit()

if (mail_str != "") or something_removed:
	f = open(config_dump_filename, 'w')
	f.write(json.dumps(theses_dict))
	f.close()
