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
CEMappingFileName = "ce_mapping.json"
ECMappingFileName = "ec_mapping.json"
CEFrameMappingFile = codecs.open(CEMappingFileName, "r")
CEFrameMappingDic = json.loads(CEFrameMappingFile.read())

ECFrameMappingFile = codecs.open(ECMappingFileName, "r")
ECFrameMappingDic = json.loads(ECFrameMappingFile.read())

a = []
for (k, v) in ECFrameMappingDic.items():
	a.append(v)

for (k, v) in CEFrameMappingDic.items():
	if k not in a:
		print k
