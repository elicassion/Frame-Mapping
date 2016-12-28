# -*- coding:utf8 -*-
import codecs
import json
import re
import os
import urllib
import urllib2
import urlparse
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from bs4 import BeautifulSoup

jpUrlRoot = 'http://sato.fm.senshu-u.ac.jp/'
jpLuUrlRoot = 'http://sato.fm.senshu-u.ac.jp/frameSQL/jfn23/menu2/'
firstCharSet = 'abcdefghijklmnopqrstuvwxyz'
engFrames = []
desFileName = 'engFrames_usedin_jp.txt'
def getPage(url):
	try:
		res = urllib2.urlopen(url, timeout = 3)
		content = res.read()
	except:
		return ''
	else:
		return content

def dealLuDetail(url):
	content = getPage(url)
	parsedContent = BeautifulSoup(content, "html.parser")
	tags = parsedContent.findAll("a", href=re.compile("^/frameSQL/jfn23/frame/"))
	# print len(tags)
	for tag in tags:
		href = tag.get('href')
		# print href
		frameName = href.split('/')[-1].replace('.html', '')
		# print frameName
		if not frameName in engFrames:
			engFrames.append(frameName)

for ch in firstCharSet:
	luUrl = jpLuUrlRoot+ch+'.html'
	content = getPage(luUrl)
	parsedContent = BeautifulSoup(content, "html.parser")
	aTags = parsedContent.findAll("a", href=re.compile("^/"))
	for aTag in aTags:
		href = aTag.get('href')
		#print href
		luDetailUrl = urlparse.urljoin(jpUrlRoot, href)
		#print luDetailUrl
		dealLuDetail(luDetailUrl)
	# break

f = codecs.open(desFileName, "w")
for name in engFrames:
	f.write(name+'\n')
print len(engFrames)
