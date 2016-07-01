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

fnFramesNamesFileName = "fn_frames_name.txt"
fnFramesNames = []
fnFramesNamesFile = codecs.open(fnFramesNamesFileName, "r")
for line in fnFramesNamesFile:
	fnFramesNames.append(line.replace("\n", ""))
fnFramesNamesFile.close()
#print fnFramesNames

cfnFrameRootDir = "D:\\GitHub\\CFN-Crawler\\cfn_frame"
cfnFrameNonExistNames = []
cfnFrameNonExistFileName = "nonexistence.txt"
cfnFrameNonExistFile = codecs.open(os.path.join(cfnFrameRootDir, cfnFrameNonExistFileName), "r")
for line in cfnFrameNonExistFile:
	cfnFrameNonExistNames.append(int(line))
cfnFrameNonExistFile.close()

CEMappingFileName = "ce_mapping.json"
ECMappingFileName = "ec_mapping.json"
nonMappingFileName = "non_mapping.txt"
CEDict = {}
ECDict = {}
nonMappingFrames = []
nonMappingFrameNames = []



for parent, dirnames, filenames in os.walk(cfnFrameRootDir):
	for filename in filenames:
		if ".json" not in filename:
			continue
		cfnFrameFile = codecs.open(os.path.join(cfnFrameRootDir, filename), "r")
		jFrameInfo = cfnFrameFile.read()
		frameInfoDic = json.loads(jFrameInfo)
		eName = frameInfoDic["fdInfo"]["eName"]
		cName = frameInfoDic["fdInfo"]["cName"]

		flag = False
		for fnName in fnFramesNames:
			fnNameLower = fnName.lower()
			fnNameUnder = fnName.replace("_","").lower()
			eNameRs = eName.replace("'s", "").lower()
			eNameUnder = eName.replace("_","").lower()
			if eName.lower() == fnNameLower or eNameRs == fnNameLower or eNameUnder == fnNameUnder:
				CEDict[cName] = fnName
				ECDict[fnName] = cName
				flag = True
				break
		if not flag:
			nonMappingFrames.append(cName)
			nonMappingFrameNames.append(eName)

nonMappingFile = codecs.open(nonMappingFileName, "w")
for i in range(0, len(nonMappingFrames)):
	nonMappingFile.write(str(nonMappingFrames[i])+"\t"+str(nonMappingFrameNames[i])+"\n")
nonMappingFile.close()
print "Non-mapping: ", str(len(nonMappingFrames))

CEMappingFile = codecs.open(CEMappingFileName, "w")
CEMappingFile.write(json.dumps(CEDict, indent = 4, sort_keys = True, ensure_ascii = False))
CEMappingFile.close()
ECMappingFIle = codecs.open(ECMappingFileName, "w")
ECMappingFIle.write(json.dumps(ECDict, indent = 4, sort_keys = True, ensure_ascii = False))
ECMappingFIle.close()