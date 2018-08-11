from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import shutil
import json

adblock = r'C:\Users\makut\Documents\SABR\Extensions\3.30.1_0'

chrome_options = Options()
chrome_options.add_argument('load-extension=' + adblock)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.create_options()

with open('config/urls.json') as f:
	data = json.load(f)

	for url in data:
		#if (url["category"] == "Pitch Value" or url["category"] == "Pitch Type"):
		driver.get('https://www.fangraphs.com/' + url["url"])
		driver.find_element_by_xpath('//*[@id="LeaderBoard1_cmdCSV"]').click()

		time.sleep(5)

		shutil.move("c:/Users/makut/Downloads/FanGraphs Leaderboard.csv", "c:/Users/makut/Documents/Data/Fangraphs/" + url["type"] + "/" + url["year"] + "/" + url["category"] + " " + url["type"] + " Data.csv")

driver.close()