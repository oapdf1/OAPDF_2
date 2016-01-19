#! /usr/bin/env python

import os,sys,glob,time
import re, requests,urllib2,json
requests.packages.urllib3.disable_warnings()

def doidecompose(suffix):
	lens=len(suffix)
	if (lens<=5):
		return ""
	layer=(lens-1)/5
	dirurl=""
	for i in range(layer):
		## In window, dir name can't end at '.'
		dirurl += suffix[i*5:(i+1)*5].rstrip('.')+"/"
	return dirurl

def quotefileDOI(doi):
	'''Quote the doi name for a file name'''
	return urllib2.quote(doi,'+/()').replace('/','@')

def unquotefileDOI(doi):
	'''Unquote the doi name for a file name'''
	return urllib2.unquote(doi.replace('@','/'))

def maxissn(issns):
	maxpre=0
	maxsuf=0
	maxnum=0
	for i in range(len(issns)):
		tmp=issns[i].split('-')
		if (int(tmp[0])>maxpre):
			maxpre=int(tmp[0])
			maxsuf=int(tmp[1])
			maxnum=i
			continue
		elif(int(tmp[0]) == maxpre and int(tmp[1]) >maxsuf):
			maxpre=int(tmp[0])
			maxsuf=int(tmp[1])
			maxnum=i
			continue
	return issns[maxnum]


def getpdfdir(doi):
	'''Get only the larger issn, should normal doi'''
	try:
		r=urllib2.urlopen('https://api.crossref.org/works/'+doi)
		j=json.loads(r.read())
		item=j['message']
		volume=item.get('volume','0')
		issue=item.get('issue','0')
		issn=maxissn(item.get('ISSN',['9999-9999']))
		return issn+os.sep+volume+os.sep+issue+os.sep
	except:
		return ""
	
for f in glob.iglob('10.*/10.*.pdf'):
	os.renames(f,)