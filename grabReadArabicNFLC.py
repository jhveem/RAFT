import requests
import pyperclip
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import os

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
	
def getTextFromLink(driver, linkList, difficulty):
	dir = 'C:\\Users\\maste\\Desktop\\arabicScraperOutput'
	count = 0
	for link in linkList:
		filename = "NFLC_" + str(difficulty)+str(count) + ".txt"
		url = 'http://readarabic.nflc.org/contents/' + str(link.find('a').get('href'))
		#print(url)
		driver.get(url)
		driver.switch_to.alert.accept()
		driver.execute_script('GoTo(1)')
		driver.switch_to.frame('mainFrame')
		#driver.switch_to.frame('40832040fdca9c5057cfe658b00bf619')
		#print(driver.page_source)
		moduleHTML = driver.page_source
		moduleSoup = BeautifulSoup(moduleHTML, "html.parser")
		#print(moduleHTML)
		sourceText = moduleSoup.find('font',{'class':'target'}).contents
		pyperclip.copy(str(sourceText))
		myFileName = os.path.join(dir, filename)
		fout = open(myFileName, "w+",encoding='utf8')
		fout.write("<DIFFICULTY>"+str(difficulty)+"</DIFFICULTY>\n")
		fout.write("<BODY>\n")
		for content in sourceText:
			if (str(content) != '<br/>'):
				fout.write(str(content) + "\n")
		fout.write("</BODY>\n")
		count += 1
		fout.close()
		
if __name__ == "__main__":
	driver = webdriver.Chrome()
	for i in range(1,4):
		
		linkList = getLinks(driver, i)
		getTextFromLink(driver, linkList, i)
	