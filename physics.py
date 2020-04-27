import os 
import requests 
import json
import array
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

URL = "https://foothill.edu/psme/marasco/4dlabs/4dlab1.html"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome("D:/Users/bismu/Downloads/ChromeDriver/chromedriver", options=options)

altitude_multiples = 100
timeOfMeasurement = 30
velocity = 0.95
max_altitude = 900

for i in range(1,int(max_altitude/altitude_multiples) + 1):
    
    driver.execute_script("window.open();")

    driver.switch_to_window(driver.window_handles[i])

    #Search for the graduation rate
    driver.get(URL)
    result_element = driver.find_element_by_name("alt")
    result_element.send_keys(str(i * altitude_multiples))
    result_element = driver.find_element_by_name("sec")
    result_element.send_keys(str(timeOfMeasurement))
    result_element = driver.find_element_by_name("v")
    result_element.send_keys(str(velocity))

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/form/input[4]").click()


filename = "results.csv"
with open(filename, 'w', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile)
    for a in range(1,int(max_altitude/altitude_multiples) + 1):
        i = 10 - a
        driver.switch_to_window(driver.window_handles[i])

        while(driver.find_element_by_name("duration").get_attribute('value') != str(timeOfMeasurement)):
            time.sleep(1)
        csvwriter.writerow([str(i * altitude_multiples), driver.find_element_by_name("D1_T").get_attribute('value'),driver.find_element_by_name("D2_T").get_attribute('value')])


