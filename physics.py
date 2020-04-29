import os 
import requests 
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#VARIABLES TO BE CHANGED##################################################
altitude_multiples = 100 
min_altitude = 100
max_altitude = 300       

velocity_multiples = 0.05
min_velocity = 0.85
max_velocity = 0.95    

timeOfMeasurement = 10

filename = "results.csv" #Exports data to this file in directory of py script
chromedriverPath = "C:/Users/[USERNAME]/Downloads/ChromeDriver/chromedriver" #Step for this in readme

run_headless = True #Set to false if you want to see all the tabs being opened
##########################################################################

URL = "https://foothill.edu/psme/marasco/4dlabs/4dlab1.html"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
if run_headless == True:
    options.add_argument('--headless')

#Opens a chrome browser window
driver = webdriver.Chrome(chromedriverPath, options=options)
rows = [["Altitude", "Muons at D1", "Muons at D2"]]
#Find out how many velocity data points we're taking, and at which altitudes
num_altitude_iterations = round((max_altitude - min_altitude) /altitude_multiples) + 1
num_velocity_iterations = round((max_velocity - min_velocity) / velocity_multiples) + 1

for velocity_iter in range(num_velocity_iterations):
    for altitude_iter in range(num_altitude_iterations):
        #Value of the velocity and altitude for the current iteration
        iteration_velocity = velocity_iter * velocity_multiples + min_velocity
        iteration_altitude = altitude_iter * altitude_multiples + min_altitude

        #Open a new tab, print a progress message, sned the values to the appropriate fields in the site, and click the start button
        driver.execute_script("window.open();")

        print("Running Test- Velocity: ", iteration_velocity, " Altitude: ", iteration_altitude)
        driver.switch_to.window(driver.window_handles[altitude_iter + num_altitude_iterations * velocity_iter])

        driver.get(URL)
        result_element = driver.find_element_by_name("alt")
        result_element.send_keys(str(iteration_altitude))
        result_element = driver.find_element_by_name("sec")
        result_element.send_keys(str(timeOfMeasurement))
        result_element = driver.find_element_by_name("v")
        result_element.send_keys(str(iteration_velocity))

        driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/form/input[4]").click()

current_recording_velocity = min_velocity
for window_iter in range(num_altitude_iterations * num_velocity_iterations):
    if window_iter % num_altitude_iterations == 0:
        rows.append(["velocity", "{:.2f}".format(current_recording_velocity) + "c"])
        current_recording_velocity += velocity_multiples

    driver.switch_to.window(driver.window_handles[window_iter])

    #Ensure that the applet is done running its simulation
    while(driver.find_element_by_name("duration").get_attribute('value') != str(timeOfMeasurement)):
        time.sleep(1)

    print("Done recording data point: ", window_iter + 1, "/", num_altitude_iterations * num_velocity_iterations)
    #Record the results of the Muons detected 
    rows.append([(window_iter % num_altitude_iterations) * altitude_multiples + min_altitude,
                  driver.find_element_by_name("D1_T").get_attribute('value'),
                  driver.find_element_by_name("D2_T").get_attribute('value')])

#Export all the data to a csv file openable through Excel
with open(filename, 'w', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile)            
    csvwriter.writerows(rows)
