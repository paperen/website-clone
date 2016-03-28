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
		if  r == None :
			self._root = sys.path[0] + os.path.sep + self._domain.replace('/', os.path.sep).strip(os.path.sep)+os.path.sep
		else :
			self._root = r+os.path.sep
		self.create_dir(self._root,True)

	# 爬取文件 & 建立目录
	def get(self,something):
		d = self.create_dir(something.replace('http://'+self._domain, ''),False)
		if d[1] != '' and d[1] != None:
			data = self.read(something)
			self.save(data,d[0]+d[1])

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
		if url.find('http://'+self._domain) == -1:
			url = 'http://'+self._domain+'/'+url
		f = self._op.open(url)
		return f.read()

	def save(self,data,filename):
		fp = open(filename, 'wb')
		fp.write(data)
		fp.close()

	def getroot(self):
		return self._root

	def parse_css(self,url,data):
		t = url.split('/')
		t.pop()
		url = "/".join(t)+'/'
		img = re.findall(r"url\((.*?)\)", data)
		for v in img:
			self.get(url+v)
		 