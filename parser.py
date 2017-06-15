#!/usr/bin/env python
# coding=utf-8

import sys
import urllib.request
import re
import csv
from bs4 import BeautifulSoup

input_file = sys.argv[1]
output_file = 'links.csv'
pages_title = 'wikipedia_page'
links_title = 'link'

def get_link(url=None):
	"""Return site url by wikipedia page.
	Params:
		url - wikipedia page url
	Return:
		href - site url
	"""
	link = None
	try:
		response = urllib.request.urlopen(url)
		html = response.read()
		soup = BeautifulSoup(html, 'lxml')
		# find infobox table
		table = soup.find("table", { "class" : "infobox" })
		# find in this table element with class url
		th = table.find(True, {"class": "url"}) 
		if not th:
			# if class was not founded, find <a> with href and rel
			th = soup.find("a", { "rel" : "nofollow" })
		th_str = str(th)
		# find in element link by regex
		link = re.findall(r"href=\"(.+?)\"", th_str)[0]
	finally:
		return link

def read_pages():
	"""Read csv file and return all wikipedia pages.
	Return:
		pages - list of wikipedia pages
	"""
	pages = []
	with open(input_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			pages.append(row[pages_title])	
	return pages

def write_pages(data):
	"""Write data to csv.
	Params:
		data - dict of data: {'wikipedia_page': 'link'}
	"""
	with open(output_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=[pages_title, links_title])
		writer.writeheader()

		for page, link in data.items():
			writer.writerow({pages_title: page, links_title: link})

def find_links(pages):
	"""Find links for every page.
	Params:
		pages - wikipedia pages.
	Return:
		result - dict of results: {'wikipedia_page': 'link'}
	"""
	result = dict()
	for page in pages:
		result[page] = get_link(page)
	return result


if __name__ == '__main__':
	pages = read_pages()
	data = find_links(pages)
	write_pages(data)

