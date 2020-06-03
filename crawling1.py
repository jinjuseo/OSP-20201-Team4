#!/usr/bin/python
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

import sys
from elasticsearch import Elasticsearch
import json

es_host="127.0.0.1"
es_port="9200"


words = []
frequencies = []


def del_symbols(my_lines):
	marks = [',', '!',':','.','#','$','%','^','&','*','(',')','+','-','/','[',']','{','}','\\','\'',';','<','>','0','1','2','3','4','5','6','7','8','9','\n','"','’','_','~','?','|','@','©']

	lines_list =[]
	for lines in my_lines:
		line = lines.text
		lines_list.append(line)

	for i in range(len(lines_list)):
		for mark in marks:
			lines_list[i] = lines_list[i].replace(mark,' ')
	
	return lines_list


def add_word(my_lines):

	
	for lines in my_lines:
		line_list=lines.split()
		for i in range(len(line_list)):
			if line_list[i] not in words:
				words.append(line_list[i])
				frequencies.append(1)
			else:
				f_index = words.index(line_list[i])
				frequencies[f_index] = frequencies[f_index] + 1



	
if __name__ == '__main__':

	url = u'http://attic.apache.org/'
	res = requests.get(url)
	html = BeautifulSoup(res.content, "html.parser")
	
	my_lines1 = html.select( 'body')
	#my_lines2 = html.select( 'body > div > div > div > h3')
	#my_lines3 = html.select('p')
	
	list1 = del_symbols(my_lines1)
	#list2 = del_symbols(my_lines2)
	#list3 = del_symbols(my_lines3)

	add_word(list1)
	#add_word(list2)
	#add_word(list3)

	print(words)
	print(frequencies)
	print(len(words),len(frequencies))

	dic = dict(url=url, words = words, frequencies = frequencies, wordcnt = len(words),processing_time = ptime,TF_IDF = tflist)
	e = json.dumps(dic)

	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)

	res = es.index(index='osp_project', doc_type='url', id=1, body=e)
	print(res)
		

	
	
