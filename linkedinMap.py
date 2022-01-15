from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

import os 
import time
import wget
import shutil

def linkedinSearch(targetName):
    s=Service("") #PUT PATH OF GECKODRIVER HERE
    driver = webdriver.Firefox(service=s)

    #Attributes to retrieve
    job = ""
    location = ""
    workingPlace = ""
    info = ""
    experiencesTab = []
    educationTab = []

    ########## LINKEDIN ##########
    driver.get('https://linkedin.com/')

    # Getting input
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@autocomplete='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='session_password']")))
    username.clear() #clearing username input field
    password.clear() #clearing password input field

    #Adding username password
    username.send_keys("") # PUT USERNAME OF LINKEDIN HERE
    password.send_keys("") # PUT PASSWORD OF LINKEDIN HERE

    # Login
    time.sleep(2)
    buttonLog = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section[1]/div/div/form/button")))
    buttonLog.click()

    # Search field
    keyword = targetName


    # Search for a profile in english
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search']"))).send_keys(keyword)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search']"))).send_keys(Keys.ENTER)

    except:
        print("[-] No english version working for search bar, trying french ...")

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Recherche']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Recherche']"))).send_keys(keyword)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Recherche']"))).send_keys(Keys.ENTER)
        print("[+] French version working for search bar, continue the program...")
    except:
        print("[-] No french version working. Program exit.")


    # Go to the first profile
    try:
        elems = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.search-results-container [href]")))
        links = [elem.get_attribute('href') for elem in elems]
        if(len(links)>0):
            first_link = links[0]
            driver.get(first_link)
    except:
        print("[-] An error has occured going to the first profile of a person. Program exit.")





    # Now we are suppoded to be on the profile of someone, we can begin retrieve information

    # Need to scroll down to the end of the page:
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    time.sleep(3)

    # Loading beautiful soup
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')


    # Get the job
    try:
        job = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").text
        #elem = WebDriverWait(driver,10).until(EC.element_located_to_be_selected((By.CSS_SELECTOR, "div.text-body-medium")))
        print("Job found : " + job)
    except:
        print("[-] No job found.")

    # Get the location
    try:
        location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small:nth-child(1)").text
        #elem = WebDriverWait(driver,10).until(EC.element_located_to_be_selected((By.CSS_SELECTOR, "div.text-body-medium")))
        print("Location found : " + location)
    except:
        print("[-] No location found.")


    # Get the working place
    try:
        workingPlace = driver.find_element(By.CSS_SELECTOR, "div.inline").text
        #elem = WebDriverWait(driver,10).until(EC.element_located_to_be_selected((By.CSS_SELECTOR, "div.text-body-medium")))
        print("Working place found : " + workingPlace)
    except:
        print("[-] No working place found.")


    # Get the working place
    try:
        info = driver.find_element(By.CSS_SELECTOR, "div.inline-show-more-text:nth-child(2)").text
        #elem = WebDriverWait(driver,10).until(EC.element_located_to_be_selected((By.CSS_SELECTOR, "div.text-body-medium")))
        print("Info found : " + info)
    except:
        print("[-] No info found.")

        
    # Experience section
    try:
        exp_section = soup.find('section', {'id': 'experience-section'} )
        exp_section = exp_section.find('ul')
        a_tags = exp_section.find_all('a')

        for a_tag in a_tags:
            job_title = a_tag.find('h3').get_text().strip()
            print("Job title : " + job_title)

            company = a_tag.find_all('p')[1].get_text().strip()
            print("Company : " + company)

            dateJob = a_tag.find_all('h4')[0].find_all('span')[1].get_text().strip()
            print("Date job : " + dateJob)

            locationJob = a_tag.find_all('h4')[2].find_all('span')[1].get_text().strip()
            print("Location Job : " + locationJob)

            experiencesTab.append("[JOB TITLE] : " + str(job_title) + " ; [COMPANY] : " + str(company) + " ; [DATE JOB] : " + str(dateJob) + " ; " + " ; [LOCATION JOB] : " + str(locationJob)) 

    except:
        print("[-] No experience section found")


    # Education section

    try:
        education = soup.find('section', {'id': 'education-section'}).find('ul')
        educations_all = education.find_all('li')
        for edall in educations_all:
            school_name = edall.find('h3').get_text()
            print("School name : " + school_name)

            educations_p = edall.find_all('p')

            try:
                degree_name = educations_p[0].find_all('span')[1].get_text().strip()
                print("Degree name : " + degree_name)

                field_name = educations_p[1].find_all('span')[1].get_text().strip()
                print("Field name : " + degree_name)

                dates = educations_p[2].find_all('span')[1].get_text().strip()
                print("Dates : " + dates)

                educationTab.append("[SCHOOL NAME] : " + school_name + " ; [DEGREE & FIELD NAME] : " + degree_name + " " + field_name + " ; [DATES] : " + dates)
            except:
                degree_field_name = educations_p[0].find_all('span')[1].get_text().strip()
                print("Degree Field name : " + degree_field_name)

                dates = educations_p[1].find_all('span')[1].get_text().strip()
                print("dates : " + degree_name)

                educationTab.append("[SCHOOL NAME] : " + school_name + " ; [DEGREE & FIELD NAME] : " + degree_field_name + " ; [DATES] : " + dates)
    except:
        print("[-] No education section found")




    print("\n---FINAL RESULTS---\n")

    print("JOB : " + job)
    print("LOCATION : " + location)
    print("WORKING PLACE : " + workingPlace)
    print("INFO : " + info)

    for el in experiencesTab:
        print(el)

    for el in educationTab:
        print(el)

    driver.close()
    return [job, location, workingPlace, info, experiencesTab, educationTab]