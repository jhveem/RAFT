import requests
import pyperclip
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import os
import re

def getLinks(driver):
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	searchResults = soup.find_all('div',{'class':'lessonTitle'})
	html = ''
	for tag in searchResults:
		#print(str(tag))
		pid = tag.parent.parent
		link = str(pid.find('a').get('href'))
		level = pid.find('div').text
		level = level[6:]
		html += "https://gloss.dliflc.edu/"+str(link)+":::"+level+"\n"
	return html
'''
def getLinks(driver, num):
	html = ''
	found = -1
	currentPage = 1
	driver.get("http://readarabic.nflc.org/contents/readarabic_1_"+str(num)+"_"+str(currentPage)+".html")
	while (found == -1):
		html += driver.page_source
		currentPage += 1
		driver.get("http://readarabic.nflc.org/contents/readarabic_1_"+str(num)+"_"+str(currentPage)+".html")
		found = driver.title.find('404')
	soup = BeautifulSoup(html, "html.parser")
	return soup.find_all('p',{'class':'page-item'})
'''
def waitForAlert(driver):
	try:
		WebDriverWait(driver, 1).until(EC.alert_is_present(),
									   'Timed out waiting for PA creation ' +
									   'confirmation popup to appear.')

		alert = driver.switch_to.alert
		alert.accept()
		print("alert accepted")
		waitForAlert(driver)
	except TimeoutException:
		print("no alert")

def getTextFromLink(driver, url, difficulty, count):
	dir = 'C:\\Users\\maste\\Desktop\\arabicScraperOutput'
	filename = "gloss_" + str(count) + ".txt"
	#print(url)
	driver.get(url)
	button = driver.find_element_by_id('gloss_link_source').click()
	
	#handle alerts
	waitForAlert(driver)
	
	divs = driver.find_elements_by_id('textSource')
	driver.implicitly_wait(1)
	driver.switch_to_frame('glossIframe')
	ps = driver.find_elements_by_tag_name('p')
	
	myFileName = os.path.join(dir, filename)
	fout = open(myFileName, "w+",encoding='utf8')
	fout.write("<DIFFICULTY>"+str(difficulty)+"</DIFFICULTY>\n")
	fout.write("<BODY>\n")
	for p in ps:
		if (str(p.text) != ""):
			fout.write(str(p.text) + "\n")
	fout.write("</BODY>\n")
	fout.close()
		
if __name__ == "__main__":
	driver = webdriver.Chrome()
	driver.get("https://gloss.dliflc.edu/")
	driver.implicitly_wait(1)
	driver.find_element_by_xpath('//*[@id="LanguageSelectorInput_2"]').click()
	driver.implicitly_wait(1)
	driver.find_element_by_xpath('//*[@id="lessonSearchBtn"]').click()
	driver.implicitly_wait(1)
	html = ''
	next = ''
	while (str(next) != 'None'):
		checkHtml = driver.page_source
		soup = BeautifulSoup(checkHtml, 'html.parser')
		oldDiv = str(soup.find('div',{'class':'lessonTitle'}))
		while str(soup.find('div',{'class':'lessonTitle'})) == oldDiv:
			checkHtml = driver.page_source
			soup = BeautifulSoup(checkHtml, 'html.parser')
			#print(soup.find('div',{'class':'lessonTitle'}))
			driver.implicitly_wait(1)
			
		html += getLinks(driver)
		oldDiv = str(soup.find('div',{'class':'lessonTitle'}))
		checkHtml = driver.page_source
		soup = BeautifulSoup(checkHtml, 'html.parser')
		next = driver.find_element_by_id('nextPageLink')
		if driver.find_element_by_id('lastPageLink').is_displayed() == False:
			next = 'None'
		else:
			next.click()

	links = html.split("\n")
	count = 0
	for link in links:
		print(link)
		if link != "":
			parts = link.split(":::")
			url = parts[0]
			level = parts[1]
			getTextFromLink(driver, url, level, count)
			count += 1
	#print(html)
	#print(html)
	