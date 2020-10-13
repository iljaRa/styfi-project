#!/usr/bin/python

# /* ------------------ IMPORTS --------------------*/
# /* -----------------------------------------------*/
import sys
import re
import random
import time
from pathlib import Path
import mmap

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import requests
import os, os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import fashion_hm_selenium_lvl2 as fhs2
# /* -----------------------------------------------*/
# /* -----------------------------------------------*/
# /* This function returns the number of lines in the file */
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
first_page=1
last_page=1

store_array = ['hm_T-Shirts']
store=store_array[i]
	
url_head = 'https://www.hm.com/de'
url_tshirts = url_head + '/products/men/tshirt'
url_tshirts_sale = url_tshirts

url_array = [url_tshirts]
url='' + url_array[i]

url_visited = []

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)
driver.implicitly_wait(5)
driver.set_window_size(1100,920)
driver.implicitly_wait(5)

driver_lvl2 = webdriver.Chrome()
driver_lvl2.implicitly_wait(2)
driver_lvl2.set_window_size(1100,920)
driver_lvl2.implicitly_wait(5)

html_soup = BeautifulSoup(driver.page_source, 'html.parser')
# /* ------------------------------------------------------*/
# /* ------------------------------------------------------*/

# /* ------------------ MAKE DIRS, OPEN FILES --------------------*/
# /* -------------------------------------------------------------*/
if not os.path.exists(store):
	os.makedirs(store)
	os.makedirs(os.path.join(store, "htmls"))
if not os.path.exists(os.path.join(store, "htmls")):
	os.makedirs(os.path.join(store, "htmls"))

filename = "visited_urls.txt"
my_file = Path(os.path.join(store, filename))
if not my_file.is_file():
	url_file= open(os.path.join(store, filename),"w+")
	url_file.write("VISITED URLS\n")
	url_file.close()
	n=0
else:
	n=file_len(filename)-1

# /* -------------------------------------------------------------*/
# /* -------------------------------------------------------------*/

# /* ------------------ ITERATIVELY CRAWL ITEMS --------------------*/
# /* ---------------------------------------------------------------*/

max_pages=last_page
delta_n=0
for page in range(first_page, last_page+1):	
	url='' + url_array[i]
	
	with open(os.path.join(store, "visited_urls.txt"),"a+") as urlFile, \
     mmap.mmap(urlFile.fileno(), 0, access=mmap.ACCESS_READ) as urlS:

		driver.get(url)
		driver.implicitly_wait(5)
		
		# Save the html source for future, more detailed, scraping
		html_soup = BeautifulSoup(driver.page_source, 'html.parser')
		filename = "full_html_" + store + "_page_" + str(page) + ".html"
		html_full_file= open(os.path.join(store, filename),"w+")
		html_full_file.write("%s" % str(html_soup.contents))
		html_full_file.close()
		
		# Interact with the page to load all results
		driver.implicitly_wait(10)
		time.sleep(1)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		
		button_more=driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/div/div[4]/div/div[4]/button')
		
		test_count=0
		driver.implicitly_wait(2.5)
		if not button_more.is_enabled():
			driver.implicitly_wait(1)
		while button_more.is_enabled() and test_count<10:	
			test_count+=1
			try:
				button_more.click()
				time.sleep(1)
				button_more=driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/div/div[4]/div/div[4]/button')
				if not button_more.is_enabled():
					driver.implicitly_wait(1)
			except WebDriverException:
				print("ERROR in " + store + " and item number. Element 'button_more' is not clickable. Element src: ")
				print(button_more.get_attribute('src'))
				continue
			
		driver.execute_script("window.scrollTo(0, 100);")
			
		html_soup = BeautifulSoup(driver.page_source, 'html.parser')
		
		div1=html_soup.find('div', class_="section productList")
		
		# Get the page data
		divs2=div1.find_all('div', {'class': ['product-list-section', 'js-product-list-section']}, {'data-page'})
		
		page_id=0
		
		# Iterate over the pages
		for div2 in divs2:
			page_id+=1
			
			items=div2.find_all('div', {'class': ['product-list-item']})
			max_items=len(items)
			print("total number of items on page %s: %s" % (page_id, max_items))
		 
			# Iterate over the list of items and scrape each individually
			for item in items:
				
				if not item or not item.find('a'):
					continue
				
				driver.implicitly_wait(10)
				
				img_src = item.find('a').get('href')
				if not img_src:
					continue
				elif urlS.find(str(img_src).encode()) != -1:
					continue
				
				delta_n=delta_n+1
				if delta_n>19:
					print("delta_n = " + str(delta_n))
					time.sleep(53)
					
					delta_n=0
				
				driver_lvl2.get(img_src)
				driver_lvl2.implicitly_wait(10)
				time.sleep(1)
				driver_lvl2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				
				# Descend into the item page to get more images and infos
				html_soup_temp = BeautifulSoup(driver_lvl2.page_source, 'html.parser')
				div0_lvl2=html_soup_temp.find('div', {'id': 'images'})
				div1_lvl2=html_soup_temp.find('ul', {'id': 'product-thumbs'}).find_all('li', recursive=False)
				
				if not div0_lvl2:
					continue
				elif img_src not in url_visited:
					n+=1
					#~ print(img_src)
					urlFile.write("%d: %s\n" % (n, str(img_src)))
					lvl2_response=fhs2.selectPics(img_src, driver_lvl2, store, page, n)
					if lvl2_response==0:
						print("Successfully completed download from " + store + ", page " + str(page) + ", item number " + str(n) + ".")
					else:
						print("There was a problem with the lvl2 of " + store + ", page " + str(page) + ", item number " + str(n) + ".")

# /* ---------------------------------------------------------------*/
# /* ---------------------------------------------------------------*/

# /* ------------------ CLOSE AND QUIT --------------------*/
# /* ------------------------------------------------------*/
			
input('Press ENTER to close the automated browser')
driver_lvl2.quit()


print("-----------DONE, ALL GOOD----------- i:" + str(i))
driver.quit()
# /* ------------------------------------------------------*/
# /* ------------------------------------------------------*/
