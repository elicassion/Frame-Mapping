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
sys.setdefaultencoding("utf-8")
cfnFrameRootDir = "D:\\GitHub\\Frame-Mapping\\cfn_frame_mapped_correct_merge"
fnFrameRootDir = "D:\\SJTU\\SpeechLab\\FrameNet\\FrameNetData\\fndata-1.6\\frame"
frameMappingFileName = "ce_mapping.json"
frameMappingDic = {}

cfnLinkMapDir = "cfn_frame_mapped_v2"
if not os.path.exists(cfnLinkMapDir):
	os.mkdir(cfnLinkMapDir)
fnLinkMapDir = "fn_frame_mapped"

feMappingResultFileName = "fe_mapping_result.txt"
mappedNumbers = []
unMappedNumbers = []
noENameNumbers = []
pureUnMappedNumbers = []
unMappedFnFENumbers = []

afterCorrectDic = "result_after_correct"
if not os.path.exists(afterCorrectDic):
	os.mkdir(afterCorrectDic)
noENameDetailFileName = "noename_unmapped_detail.txt"
pureUnMappedDetailFileName = "pure_unmapped_detail.txt"
unMappedFnFEFileName = "fnfe_unmapped_detail.txt"

# noENameDetailFile = codecs.open(noENameDetailFileName, "w")
# pureUnMappedDetailFile = codecs.open(pureUnMappedDetailFileName, "w")
# unMappedFnFEFile = codecs.open(unMappedFnFEFileName, "w")

noENameDetailFile = codecs.open(os.path.join(afterCorrectDic, noENameDetailFileName), "w")
pureUnMappedDetailFile = codecs.open(os.path.join(afterCorrectDic, pureUnMappedDetailFileName), "w")
unMappedFnFEFile = codecs.open(os.path.join(afterCorrectDic, unMappedFnFEFileName), "w")

unMappedInfoSortedByFrameArray = []
def init():
	global frameMappingDic
	frameMappingFile = codecs.open(frameMappingFileName, "r")
	frameMappingDic = json.loads(frameMappingFile.read())
	frameMappingFile.close()

def readCfn(cName):
	cfnFrameFileName = os.path.join(cfnFrameRootDir, cName+".json")
	cfnFrameFile = codecs.open(cfnFrameFileName, "r")
	s = cfnFrameFile.read()
	cfnFrameFile.close()
	return s

def readFn(eName):
	fnFrameFileName = os.path.join(fnFrameRootDir, eName+".xml")
	fnFrameFile = codecs.open(fnFrameFileName, "r")
	s = fnFrameFile.read()
	fnFrameFile.close()
	return s

def removeTag(string):
	return re.compile('<[^>]+>').sub("", string)#.split("\n")[0]

def extractFnFE(fnFrameDic):
	fnFENames = []
	fnFEIsCore = []
	fnFEAbbr = []
	fnFEDef = []
	fnFEs = fnFrameDic["frame"]["FE"]
	for fnFE in fnFEs:
		if fnFE["@name"] in fnFENames:
			continue
		fnFENames.append(fnFE["@name"])
		fnFEIsCore.append(True if fnFE["@coreType"] == "Core" else False)
		fnFEAbbr.append(fnFE["@abbrev"] if not fnFE["@abbrev"] == "" else None)
		fnFEDef.append(removeTag(fnFE["definition"]))
	return fnFENames, fnFEIsCore, fnFEAbbr, fnFEDef

def judgeMapping(src, dst):
	if src.lower() == dst.lower() or \
		src.replace("_", "").lower() == dst.replace("_", "").lower():
		return True
	else:
		return False

def cmp_cfnfe(fe1, fe2):
	isMap1 = fe1["isMapped"]
	isMap2 = fe2["isMapped"]
	isCore1 = fe1["isCore"]
	isCore2 = fe2["isCore"]
	if isMap1 and not isMap2:
		return -1
	elif isMap1 and isMap2:
		if isCore1 and not isCore2:
			return -1
		else:
			return 1
	else:
		return 1

def writeMappedFile(name, dic):
	dic["element"].sort(cmp_cfnfe)
	mappedFileName = os.path.join(cfnLinkMapDir, name+".json")
	mappedFile = codecs.open(mappedFileName, "w")
	mappedFile.write(json.dumps(dic, ensure_ascii = False, indent = 4))
	mappedFile.close()

def writeUnMappedFile(fname, ne, pure):
	if len(ne) > 0:
		noENameDetailFile.write(fname+": \n")
		for i in ne:
			noENameDetailFile.write("\t"+i+"\n")

	if len(pure) > 0:
		pureUnMappedDetailFile.write(fname+": \n")
		for i in pure:
			pureUnMappedDetailFile.write("\t"+i+"\n")

def writeUnMappedFnFEFile(efname, cfname, felist):
	if len(felist) > 0:
		unMappedFnFEFile.write(efname+"\t"+cfname+": \n")
		for i in felist:
			unMappedFnFEFile.write("\t"+i+"\n")

def addSortedByFrameDict(cName, eName, unMpdFnFEList, noENameFEList, pureUnMappedFEList):
	unMappedInfoSortedByFrameDict = {}
	unMappedInfoSortedByFrameDict["cName"] = cName
	unMappedInfoSortedByFrameDict["eName"] = eName
	unMappedInfoSortedByFrameDict["fnfelist"] = unMpdFnFEList
	unMappedInfoSortedByFrameDict["nonenamefelist"] = noENameFEList
	unMappedInfoSortedByFrameDict["purefelist"] = pureUnMappedFEList
	unMappedInfoSortedByFrameArray.append(unMappedInfoSortedByFrameDict)

def cmpframe(f1, f2):
	return f1["cName"] < f2["cName"]

def writeSortedByFrame():
	filename = "frame_to_correct.txt"
	file = codecs.open(os.path.join(afterCorrectDic, filename), "w")
	unMappedInfoSortedByFrameArray.sort(cmpframe)
	fcode = 0
	for fm in unMappedInfoSortedByFrameArray:
		if len(fm["fnfelist"]) == 0 and len(fm["nonenamefelist"]) == 0 and len(fm["purefelist"]) == 0:
			continue
		fcode += 1
		file.write(fm["cName"]+"\t"+fm["eName"]+"\t"+str(fcode)+"\n")
		if len(fm["fnfelist"]) > 0:
			file.write("\tCFN not included: \n")
			for fe in fm["fnfelist"]:
				file.write("\t\t"+fe+"\n")
		if len(fm["nonenamefelist"]) > 0:
			file.write("\tNo English Name: \n")
			for fe in fm["nonenamefelist"]:
				file.write("\t\t"+fe+"\n")
		if len(fm["purefelist"]) > 0:
			file.write("\tPure UnMapped: \n")
			for fe in fm["purefelist"]:
				file.write("\t\t"+fe+"\n")
		file.write("\n")
	file.close()



init()
for (cName, eName) in frameMappingDic.items():
	#print cName, eName
	cfnFrameDic = json.loads(readCfn(cName))
	fnFrameDic = xmltodict.parse(readFn(eName))

	fnFENames, fnFEIsCore, fnFEAbbr, fnFEDef = extractFnFE(fnFrameDic)
	mpdNumber = 0
	noENameNumber = 0
	noENameFEList = []
	pureUnMappedFEList = []
	mpdFnFEId = []
	for cfnFE in cfnFrameDic["element"]:
		flag = False
		for i in range (0, len(fnFENames)):
			if cfnFE["eName"] == None:
				flag = False
				noENameNumber += 1
				break
			if judgeMapping(cfnFE["eName"], fnFENames[i]):
				cfnFE["isMapped"] = True
				cfnFE["isCore"] = fnFEIsCore[i]
				mpdNumber += 1
				flag = True
				mpdFnFEId.append(i)
				break
		if not flag:
			cfnFE["isMapped"] = False
			cfnFE["isCore"] = False
			if cfnFE["eName"] == None:
				noENameFEList.append(cfnFE["cName"])
			else:
				pureUnMappedFEList.append(cfnFE["cName"])

	unMpdNumber = len(cfnFrameDic["element"]) - mpdNumber
	pureUnMappedNumber = unMpdNumber - noENameNumber
	mappedNumbers.append(mpdNumber)
	unMappedNumbers.append(unMpdNumber)
	noENameNumbers.append(noENameNumber)
	pureUnMappedNumbers.append(pureUnMappedNumber)
	

	unMpdFnFEList = []
	for i in range(0, len(fnFENames)):
		if i not in mpdFnFEId:
			unMpdFnFEList.append(fnFENames[i])
			newFEDict = {}
			newFEDict["abbrName"] = fnFEAbbr[i]
			newFEDict["eName"] = fnFENames[i]
			newFEDict["isMapped"] = False
			newFEDict["cName"] = None
			newFEDict["isCore"] = fnFEIsCore[i]
			newFEDict["def"] = fnFEDef[i]
			cfnFrameDic["element"].append(newFEDict)
	unMappedFnFENumbers.append(len(unMpdFnFEList))

	writeUnMappedFnFEFile(eName, cName, unMpdFnFEList)
	writeMappedFile(cName, cfnFrameDic)
	writeUnMappedFile(cName, noENameFEList, pureUnMappedFEList)
	addSortedByFrameDict(cName, eName, unMpdFnFEList, noENameFEList, pureUnMappedFEList)

	#break

feMappingResultFile = codecs.open(os.path.join(afterCorrectDic, feMappingResultFileName), "w")
feMappingResultFile.write("Mapped FEs: "+str(sum(mappedNumbers))+"\n")
feMappingResultFile.write("UnMapped CFN FEs: "+str(sum(unMappedNumbers))+"\n")
feMappingResultFile.write("No English Name CFN FEs: "+str(sum(noENameNumbers))+"\n")
feMappingResultFile.write("Pure UnMapped CFN FEs: "+str(sum(pureUnMappedNumbers))+"\n")
feMappingResultFile.write("UnMapped FN FEs: "+str(sum(unMappedFnFENumbers))+"\n")

feMappingResultFile.close()
noENameDetailFile.close()
pureUnMappedDetailFile.close()
writeSortedByFrame()
	
