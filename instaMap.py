from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait

import os 
import time
import wget
import shutil

def instaSearch(targetName):
    s=Service("") #PUT PATH OF GECKODRIVER HERE
    driver = webdriver.Firefox(service=s)

    ########## INSTAGRAM ##########
    driver.get('https://www.instagram.com/')

    # cookie - try english version, otherwise french
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[text()='Accept']")
        cookie_button.click()
    except:
        print("[-] No english version working for accept button, trying french ...")

    try:
        print("[+] French version found for accept button. Program continue...")
        cookie_button = driver.find_element(By.XPATH, "//button[text()='Accepter tout']")
        cookie_button.click()
    except:
        print("[-] No french version working for accept button. Program continue...")
        exit


    # Getting input
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear() #clearing username input field
    password.clear() #clearing password input field

    #Adding username password
    username.send_keys("") # PUT USERNAME OF INSTA HERE
    password.send_keys("") # PUT PASSWORD OF INSTA HERE

    #Log in button
    time.sleep(2) # Otherwise, another button obscures this submit button
    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Not now button
    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    except:
        print("[-] No english version working for Not Now button, trying french ...")

    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Plus tard')]"))).click()
        print("[+] French version found for accept button. Program continue...")
    except:
        print("[-] No french version working for Not Now button. Program exit.")


    # Not now button
    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    except:
        print("[-] No english version working for Not Now button, trying french ...")

    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Plus tard')]"))).click()
        print("[+] French version found for accept button. Program continue...")
    except:
        print("[-] No french version working for Not Now button. Program exit.")


    # Search field
    try:
        searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    except:
        print("[-] No english version working for placeholder search, trying french ...")

    try:
        searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Rechercher']")))
        print("[+] French version found for placeholder search. Program continue...")
    except:
        print("[-] No french version working for placeholder search. Program exit.")


    searchbox.clear()
    keyword = targetName
    searchbox.send_keys(keyword)
    time.sleep(2)

    # Press enter
    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)

    # Scroll through pictures
    time.sleep(5)

    #scroll down 3 times
    #increase the range to sroll more
    n_scrolls = 3
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    images = driver.find_elements(By.TAG_NAME, 'img')
    images = [image.get_attribute("src") for image in images]

    # Create folder to save images
    nameFolderAndFiles = "target"
    path = os.getcwd()
    path = os.path.join(path, nameFolderAndFiles)
    #Deleting the folder and its files in case it already exists:
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("No folder to remove")
    os.mkdir(path)
    time.sleep(2)

    # Save images
    counter = 0
    for image in images:
        save_as = os.path.join(path, nameFolderAndFiles + str(counter) + ".jpg")
        wget.download(image, save_as)
        counter += 1

    driver.close()