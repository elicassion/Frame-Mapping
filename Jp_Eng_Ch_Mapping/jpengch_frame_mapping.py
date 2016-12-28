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
jcMappingFileName = 'jc_mapping.json'
ecMappingFileName = '../ec_mapping.json'
ecMappingFile = codecs.open(ecMappingFileName, "r")
engFramesInJpFileName = 'engFrames_usedin_jp.txt'
engFramesInJpFile = codecs.open(engFramesInJpFileName, "r")
ecMappingDic = json.loads(ecMappingFile.read())
jcMappingDic ={}
mappedFrameNumber = 0
for line in engFramesInJpFile:
	line = line.strip()
	if ecMappingDic.has_key(line):
		jcMappingDic[line] = ecMappingDic[line]
		mappedFrameNumber += 1
jcMappingFile = codecs.open(jcMappingFileName, "w")
jcMappingFile.write(json.dumps(jcMappingDic, ensure_ascii = False, sort_keys = True, indent = 4))
ecMappingFile.close()
engFramesInJpFile.close()
jcMappingFile.close()
print mappedFrameNumber