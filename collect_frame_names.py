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

filename = "fn_frames_name.txt"
rootDir = "D:\\SJTU\\SpeechLab\\FrameNet\\FrameNetData\\fndata-1.6\\frame"
file = codecs.open(filename, "w")
for parent, dirnames, filenames in os.walk(rootDir):
	for filename in filenames:
		file.write(filename.split(".")[0] + "\n")

