#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from nltk import word_tokenize
from nltk.corpus import stopwords

import sys
from elasticsearch import Elasticsearch
import json
import time

es_host="127.0.0.1"
es_port="9200"


words = []
frequencies = []
word_d = {}


def del_symbols(my_lines):
	marks = [',', '!',':','.','#','$','%','^','&','*','(',')','+','-','/','[',']','{','}','\\','\'',';','<','>','0','1','2','3','4','5','6','7','8','9','\n','"','’','_','~','?','|','@','©']
	h = 0
	lines_list =[]
	for text in my_lines:
		#line = lines.text
		lines_list.append(text)
		h = h+1

	for i in range(len(lines_list)):
		for mark in marks:
			lines_list[i] = lines_list[i].replace(mark,' ')
	
	return lines_list

def del_stopwords(lines_list):
	
	string=""
	for i in range(len(lines_list)):
		string = string + str(lines_list[i])
	

	#print("list 를 string으로 바꾼 문자열 ",string)
	swlist = []	#stopwords list
	for sw in stopwords.words("english"):
		swlist.append(sw)
	
	
	tokenized = word_tokenize(string)
	
	result = []	
	for w in tokenized:
		if w not in swlist:
			result.append(w)
	
	

	return result	#stop words 제거한 word lists

def process_timer():
	return time.time()
	

def add_word(wlist):

	

	"""for w in wlist:		# word list, freq list 분리
				
		if w not in words:
			words.append(w)
			frequencies.append(1)
		else:
			f_index = words.index(w)
			frequencies[f_index] = frequencies[f_index] + 1"""
	
	for w in wlist:		# word_d 딕셔너리에 단어, 빈도 수 추가
		if w not in word_d.keys():
			word_d[w] = 0
		word_d[w] +=1


	
def multiple(url_list):
	for url in url_list:
		start = process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = url.strip()
		ress = requests.get(urladdress)	#에러가 발생하지 않으면 f2에 url쓰기
		"""
		if urladdress not in url_cur_list:			
			if urladdress not in urllist:		
				f2.write(url)
				url_cur_list.append(urladdress)
			else:
				print("중복된 url")
				continue
				
		else:
			print("중복된 url")
			continue
		"""
			

		html = BeautifulSoup(ress.content, "html.parser")
		#content = html.select('body')
		content = html.findAll(text = True)
		#print(content)
		#print("-------------------------------------------")
		list1 = del_symbols(content)
		#print(list1)
		list1 = del_stopwords(list1)
			
		#print( "stopwords를 제거한 단어 list",list1)	
		add_word(list1)	
		end = process_timer()
		ptime = end - start #처리시간 check
		words = list(word_d.keys())			#dict.keys() -> words list
		frequencies = list(word_d.values())		#dict.values() -> frequency list
		

		dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = 		len(words),processing_time = ptime)
		e = json.dumps(dic)
		es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
		res = es.index(index='urls', doc_type='url',id=urladdress, body=e)
		print(res)
		
		words.clear()
		frequencies.clear()
		word_d.clear()

def single(url):
	start = process_timer()		
	urladdress = url.strip()	
	res = requests.get(urladdress)
	html = BeautifulSoup(res.content, "html.parser")
	#content = html.select('body')
	content = html.findAll(text = True)
	#print(content)
	#print("-------------------------------------------")
	list1 = del_symbols(content)
	#print(list1)
	list1 = del_stopwords(list1)
			
	#print( "stopwords를 제거한 단어 list",list1)	
	add_word(list1)	
	end = process_timer()
	ptime = end - start #처리시간 check
	words = list(word_d.keys())			#dict.keys() -> words list
	frequencies = list(word_d.values())		#dict.values() -> frequency list
		

	dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = 	len(words),processing_time = ptime)
	e = json.dumps(dic)
	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	res = es.index(index='urls', doc_type='url',id=urladdress, body=e)
	print(res)
		
	words.clear()
	frequencies.clear()
	word_d.clear()
			
def word_processsing(url_list):
	for url in url_list:
		start = process_timer()		
		#urladdress = 'u'+'\''+url.strip()+'\''		
		urladdress = url.strip()
		ress = requests.get(urladdress)	#에러가 발생하지 않으면 f2에 url쓰기
		"""
		if urladdress not in url_cur_list:			
			if urladdress not in urllist:		
				f2.write(url)
				url_cur_list.append(urladdress)
			else:
				print("중복된 url")
				continue
				
		else:
			print("중복된 url")
			continue
		"""
			

		html = BeautifulSoup(ress.content, "html.parser")
		#content = html.select('body')
		content = html.findAll(text = True)
		#print(content)
		#print("-------------------------------------------")
		list1 = del_symbols(content)
		#print(list1)
		list1 = del_stopwords(list1)
			
		#print( "stopwords를 제거한 단어 list",list1)	
		add_word(list1)	
		end = process_timer()
		ptime = end - start #처리시간 check
		words = list(word_d.keys())			#dict.keys() -> words list
		frequencies = list(word_d.values())		#dict.values() -> frequency list
		

		dic = dict(url=urladdress, words = words, frequencies = frequencies, wordcnt = 		len(words),processing_time = ptime)
		e = json.dumps(dic)
		es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
		res = es.index(index='urls', doc_type='url',id=urladdress, body=e)
		print(res)
		
		words.clear()
		frequencies.clear()
		word_d.clear()
		
#if __name__ == '__main__':
def main():
	#idvalue=1
	cnt =0 
	url_list = []	
	f = request.files['file']
	if f>0:
		f.save(secure_filename(f.filename))
		f1 = open(f.filename,'r')
		url_list = f1.readlines()
		f1.close()
		#multiple(url_list)
	
	else:
		url = request.form['url']
		#single(url)	
		url_list.append(url)

	word_processsing(url_list)

	"""	
	try:
		f2 = open('test_output.txt','r')
		try:
			for url in f2:
				urllist.append(url.strip())
		finally:			
			f2.close()
	except IOError:
		print('test_output.txt 파일이 존재하지 않음')

	
	f2 = open('test_output.txt','a')"""	
	
	#url_cur_list = []
	
	#여기서부터 밑의 주석까지 반복문처리 

	
	



	
	
