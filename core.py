#!/usr/bin/env
#-*- coding: UTF-8 -*-
#Filename: thief.py

import os,sys,urllib,re

class thief:
	_domain = ""
	_root = ""
	_siteurl = ""
	def __init__(self,d,r):
		self._op = urllib.FancyURLopener({})
		self._domain = d
		self._siteurl = 'http://'+self._domain+'/'
		print self._siteurl
		if  r == None :
			self._root = sys.path[0] + os.path.sep + self._domain.replace('/', os.path.sep).strip(os.path.sep)+os.path.sep
		else :
			self._root = r+os.path.sep
		self.create_dir(self._root,True)

	# 爬取文件 & 建立目录
	def get(self,something):
		something = something.replace('http://'+self._domain, '')
		something = something.replace('https://'+self._domain, '')
		if something.find('http://') != -1 or something.find('https://') != -1:
			return something
		d = self.create_dir(something,False)
		if d[1] != '' and d[1] != None:
			data = self.read(something)
			res = self.save(data,d[0]+d[1])
			if res == 0:
				return ""

			# 判断是否是CSS
			if d[1].split('.').pop() == 'css':
				self.parse_css(something,data)
		return something.replace('http://'+self._domain, '').strip('/')

	# [返回本地文件夹路径,文件名]
	def create_dir(self,d,is_root):
		if is_root:
			t = d
			f = None
		else:
			t = d.strip('/').split('/')
			f = t.pop()
			f_list = re.findall(r"^(.*?)[\?|\#].*", f)
			if f_list != [] : f = f_list[0]
			t = "/".join(t)
			t = self._root + t.replace('/', os.path.sep)
		if os.path.exists(t) == False :
			os.makedirs(t)
		return [t + os.path.sep,f]

	def read(self,url):
		if url[0:2] == '//':
			url = 'http:' + url
		elif url.find('http://'+self._domain) == -1:
			url = 'http://'+self._domain+'/'+url
		
		try:
			f = self._op.open(url)
			return f.read()
		except Exception:
			return ""

	def save(self,data,filename):
		if os.path.isdir(filename):
			return 0
		fp = open(filename, 'wb')
		fp.write(data)
		fp.close()
		return 1

	def getroot(self):
		return self._root

	def parse_css(self,url,data):
		t = url.split('/')
		t.pop()
		url = "/".join(t)+'/'
		img = re.findall(r"url\((.*?)\)", data)
		for v in img:
			v = v.strip("\"")
			if v.find('http') != -1:
				self.get(v.strip('\''))
			elif v[0:5] == 'data:':
				continue
			else:
				self.get(url+v.strip('\''))
		 