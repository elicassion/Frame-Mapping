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
sys.setdefaultencoding("utf-8")

frameMappingFileName = "ce_mapping.json"
frameMappingFile = codecs.open(frameMappingFileName, "r")
frameMappingDic = json.loads(frameMappingFile.read())
for (cName, eName) in frameMappingDic.items():
	