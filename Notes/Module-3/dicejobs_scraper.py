from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

cService = Service("/Users/sreejabolla/Downloads/chromedriver")
driver = webdriver.Chrome(service=cService)

driver.get('https://www.dice.com/jobs')
time.sleep(2)
search_box = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Job title, skill, company, keyword"]')
search_box.send_keys("machine learning engineer intern")
location = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Location Field"]')
location.send_keys("Massachusetts")
search_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="job-search-search-bar-search-button"]')
search_button.click()
jobs = []
while True:
	time.sleep(2)
	listings = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
	for i in range(len(listings)):
		info = {}
		job = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')[i]
		title = job.find_element(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')
		info["Title"] = title.text.strip()
		company = job.find_element(By.CSS_SELECTOR, 'p.mb-0.line-clamp-2.text-sm')
		info["Company"] = company.text.strip()		
		details = job.find_elements(By.CSS_SELECTOR, 'p.text-sm.font-normal.text-zinc-600')
		info["Location"] = details[0].text.strip()
		info["Date"] = details[2].text.strip()
		description = job.find_element(By.CSS_SELECTOR, 'p.line-clamp-2.h-10.shrink.grow.basis-0.text-sm.font-normal.text-zinc-900')
		info["Description"] = description.text.strip()
		link = job.find_element(By.CSS_SELECTOR, 'a[data-testid="job-search-job-detail-link"]')
		info["Link"] = link.get_attribute("href")
		jobs.append(info)
		time.sleep(1)
	next_button = driver.find_element(By.CSS_SELECTOR, 'span[aria-label= "Next"]')
	if next_button.get_attribute('data-disabled') == 'true':
		break
	driver.execute_script("arguments[0].click();", next_button)
fieldnames = ["Title", "Company", "Location", "Date", "Description", "Link"]
with open("dice_scraped.csv", "w", newline = "") as file:
	writer = csv.DictWriter(file, fieldnames = fieldnames)
	writer.writeheader()
	writer.writerows(jobs)
driver.quit()
