from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options   
import csv
import time
cService = Service("/Users/sreejabolla/Downloads/chromedriver")
driver = webdriver.Chrome(service=cService)
driver.get('https://www.touchwindow.com')
time.sleep(2)
search = driver.find_element(By.ID, "l-desktop-search")
search.send_keys("Printer")
search.send_keys(Keys.RETURN)
printer_info = []
while True:
	product_area = driver.find_element(By.ID, "js-product-list")
	products = product_area.find_elements(By.CSS_SELECTOR, "div.column.category-product")
	for product in products:
		info = {} 
		info["ID"] = product.find_element(By.CSS_SELECTOR, "span.category-product-number").text.strip()
		link = product.find_element(By.CSS_SELECTOR, 'a.category-product-image-wrapper')
		driver.execute_script("arguments[0].click();", link)
		text = driver.find_element(By.CSS_SELECTOR, "div.product-information__header.whole")
		info["Name"] = text.find_element(By.CSS_SELECTOR, "div.product-title h1").text.strip()
		price = text.find_elements(By.ID, "js-price-value")
		if len(price) == 1:
			info["Price"] = price[0].text.strip()
		info["Weight"] = text.find_element(By.CLASS_NAME, "product-weight").text.strip()
		description = text.find_elements(By.TAG_NAME, "p")
		if len(description) == 1:
			info["Description"] = description[0]
		elif len(description) > 1:
			info["Description"] = description[1]
		printer_info.append(info)
		driver.back()
		time.sleep(1)
	next = driver.find_elements(By.CLASS_NAME, "page-links-next")
	if len(next) == 1:
		next[0].click()
	else:
		break
fieldnames = ["ID", "Name", "Price", "Weight", "Description"]
with open("touchwindow_scraped.csv", "w", newline = "") as file:
	writer = csv.DictWriter(file, fieldnames = fieldnames)
	writer.writeheader()
	writer.writerows(printer_info)
