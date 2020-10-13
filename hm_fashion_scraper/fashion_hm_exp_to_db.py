#!/usr/bin/python

# /* ------------------ IMPORTS --------------------*/
# /* -----------------------------------------------*/
import sys
import re
import time
from pathlib import Path
import datetime
import json

import os, os.path
from bs4 import BeautifulSoup

import db_export as dbe
# /* -----------------------------------------------*/
# /* -----------------------------------------------*/

def file_len(fname):
	line_count_tot=0
	with open(os.path.join(store, fname)) as f:
		for line_count, l in enumerate(f):
			pass
			line_count_tot = line_count + 1
	return line_count_tot

# /* ------------------ INITIALIZATION --------------------*/
# /* ------------------------------------------------------*/
i=int(sys.argv[1])

gender_array = ['F', 'M']
gender = gender_array[i]

store='dataset_hm'

items_count=0


filename = "id.dat"
my_file = Path(os.path.join(store, filename))
if not my_file.is_file():
	sys.exit("[ABORT:] No id.dat detected! \nDoes the directiory '%s' exist?" % store)
else:
	items_count=file_len(filename)-1

print(items_count)
# /* ------------------------------------------------------*/
# /* ------------------------------------------------------*/

# /* ------------------ CREATE TABLE --------------------*/
# /* ----------------------------------------------------*/
dbe.create_t_shirt_table()
# /* ----------------------------------------------------*/
# /* ----------------------------------------------------*/

# /* ------------------ SCRAPE --------------------*/
# /* ----------------------------------------------*/
count = 1
with open(os.path.join(store, "id.dat"), "r") as id_file:
	for line in id_file:
		item_id = line.strip();
		if item_id == "":
			print("ERROR: Id is an empty string! Item from " + store + " (line = " + count + ") is not added to the data-base.")
			continue
		count+=1
		
		filename = str(item_id) +".html"
		html_path = store + '/' + "htmls"
		
		image_path = "/home/ilja/scraper/" + store + "/" + str(item_id) + "_0.jpg"
		
		print(html_path + '/' + filename)
		
		html_file = Path(os.path.join(html_path, filename))
		if not html_file.is_file():
			continue
		
		with open(os.path.join(html_path, filename), "r") as f:
			
			contents = f.read()

			soup = BeautifulSoup(contents, 'lxml')
			
			this_f_url = soup.find('link', {'rel': 'canonical'}).get('href')
			
			json_data_string = soup.find('script', {'type': 'application/ld+json'}).text
			
			infos = json.loads(json_data_string)
			
			title = infos['name'].strip()
			
			brand = infos['brand']['name'].strip()
			
			if "amp;amp;" in brand:
				brand = brand.replace("amp;amp;", "")
			
			print(brand)
			color = infos['color'].strip()
			
			price = infos['offers'][0]['price'].strip()
						
			print(str(count) + ": " + title)
			
			url=this_f_url
			
			store_name="hm"
			
			dbe.insert_into_t_shirts(item_id, url, image_path, title, store_name, gender, price)
			
		

			
print("-----------DONE, ALL GOOD-----------")

# /* ----------------------------------------------*/
# /* ----------------------------------------------*/

