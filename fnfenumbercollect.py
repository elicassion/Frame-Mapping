# -*- coding:utf8 -*-
import codecs
import json
import re
import os
import urllib
import urllib2
import urlparse
import sys
import xmltodict
reload(sys)
sys.setdefaultencoding( "utf-8" )

cnt = 0
rootDir = "D:\\SJTU\\SpeechLab\\FrameNet\\FrameNetData\\fndata-1.6\\frame"
def readFn(eName):
	fnFrameFileName = os.path.join(rootDir, eName)
	fnFrameFile = codecs.open(fnFrameFileName, "r")
	s = fnFrameFile.read()
	fnFrameFile.close()
	fnFrameDic = xmltodict.parse(s)
	if not fnFrameDic.has_key("frame"):
		return 0
	return len(fnFrameDic["frame"]["FE"])


for parent, dirnames, filenames in os.walk(rootDir):
	for filename in filenames:
		cnt += readFn(filename)

print cnt

