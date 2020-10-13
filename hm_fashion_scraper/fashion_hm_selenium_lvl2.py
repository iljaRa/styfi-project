from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import re, itertools
import requests
import os, os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse	

import random
import time
import datetime

random.seed(42)

DEBUG=False
  
def downloadImage(req, filename, storeToSave):
	with open(os.path.join(storeToSave, filename), 'wb') as the_image:
		for byte_chunk in req.iter_content(chunk_size=128*4):
			the_image.write(byte_chunk)

def export_html_file(driver, store):
	html_soup = BeautifulSoup(driver.page_source, 'html.parser')
	
	time_stamp=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	
	filename = time_stamp + ".html"
	html_path = store + '/' + "htmls"
	html_full_file= open(os.path.join(html_path, filename),"w+")
	html_full_file.write("%s" % str(html_soup.contents))
	html_full_file.close()
	
	return time_stamp

def selectPics(url, driver, store):
	time_stamp = export_html_file(driver, store)
	
	try:
		driver = load_high_res_images(driver, store, time_stamp)
		return crawlChild(url, driver, store, time_stamp)
	except AttributeError as error:
		print(error)
		raise AttributeError("ERROR in the crawler_child function 'selectPics'.")	
		return 'NULL'

def load_high_res_images(driver, store, time_stamp):
	try:
		button_close=driver.find_element_by_xpath('//*[@id="gdpr-modal"]/div[2]/button')
		if not button_close:
			print("NO BUTTON_CLOSE")
		else:
			driver.implicitly_wait(5)
			try:
				button_close.click()
			except:
				print(" ")
				#~ if DEBUG:
					#~ print(button_close.get_attribute('class'))
	except:
		print(" ")
	
	try:	
		scroller1=driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[2]/div[1]/figure[2]')
		img=scroller1.find_element_by_tag_name('img')
	except:
		print("There is only one image for this item")
	
	driver.implicitly_wait(10)
	try:
		img.click()
	except:
		if DEBUG:
			print("ERROR in " + store + " and item id " + time_stamp + ". Element is not clickable. Element class name: ")
			print(img.get_attribute('class'))
	driver.implicitly_wait(0.5)
	time.sleep(random.randint(1, 4))
	
	html_soup = BeautifulSoup(driver.page_source, 'html.parser')
	div1 = html_soup.find('div', {'class': ['module', 'product-description', 'sticky-wrapper']})
	figures=div1.find_all('figure')
	to_scroll=1
	to_scroll=len(figures)
	
	b_button_found = False
	try:
		next_button=driver.find_element_by_xpath('/html/body/div[10]/button[2]')
	except:
		print("No next button found")
	driver.implicitly_wait(10)
	try:
		next_button.click()
		time.sleep(random.randint(1, 6))
		for click in range(1, to_scroll-1):	
			next_button.click()
			time.sleep(random.randint(1, 6))	
		b_button_found=True
	except:
		if DEBUG:
			print("ERROR in " + store + " and item id " + time_stamp + ". 'Next Button' is not clickable. Element class name: ")
			print(next_button.get_attribute('class'))
	
	if not b_button_found:
		raise AttributeError("ERROR in " + store + " and item id " + time_stamp + ". High resolution images could not be loaded.")		
	return driver

def crawlChild(url, driver, store, time_stamp):
	pathOfStore = store + '/' + 'images'
	if not os.path.exists(pathOfStore):
		os.makedirs(pathOfStore)
		
	
	pathOfItem = pathOfStore + '/' + time_stamp
	if not os.path.exists(pathOfItem):
		os.makedirs(pathOfItem)
		
	with open(os.path.join(store, "id.dat"),"a") as id_file:
		id_file.write("%s\n" % time_stamp)
	
	html_soup = BeautifulSoup(driver.page_source, 'html.parser')
	pictures=html_soup.find_all('img', id=re.compile("fullscreenimage_"))
	if DEBUG and not pictures:
		print("ERROR in " + store + " and item id " + time_stamp + ". Fullscreen picture could not be displayed.")
	
	item_num=0
	for img in pictures:
		img_src = img.get('src')
		if not img_src:
			continue
		else:
			img_src="https:" + img_src
			req = requests.get(img_src, stream=True)
			filename=str(time_stamp) + "_" + str(item_num)
			downloadImage(req, filename, pathOfItem)
			item_num+=1
			time.sleep(random.randint(1, 3))
			
	return time_stamp
