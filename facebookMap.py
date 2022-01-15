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


def facebookSearch(targetName):
    s=Service("") #PUT PATH OF GECKODRIVER HERE
    driver = webdriver.Firefox(service=s)

    ########## FACEBOOK ##########
    driver.get('https://www.facebook.com/')

    # cookie - try english version, otherwise french
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[text()='Accept']")
        cookie_button.click()
    except:
        cookie_button = driver.find_element(By.XPATH, "//button[text()='Autoriser tous les cookies']")
        cookie_button.click()


    # Getting input
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    username.clear() #clearing username input field
    password.clear() #clearing password input field

    #Adding username password
    username.send_keys("") # PUT USERNAME OF FB HERE
    password.send_keys("") # PUT PASSWORD OF FB HERE

    #Log in button
    time.sleep(2) # Otherwise, another button obscures this submit button
    log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Search field
    try:
        searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    except:
        searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Rechercher sur Facebook']")))

    searchbox.clear()
    keyword = targetName
    searchbox.send_keys(keyword)
    time.sleep(2)

    # Press enter to the search field
    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)

    # Click on the person
    time.sleep(2)
    try:
        driver.find_element(By.By.XPATH, "//div[@aria-label='"+keyword+"']").click()
    except:
        "Error clicking on the person"


    # Loading beautiful soup
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    res = soup.find('div', {'aria-label':'Résultats de la recherche'})
    link = res.find('a')['href']

    # Go to new link
    driver.get(link)

    # Click on button photos
    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Photos')]"))).click()
    except:
        print("[-] No english version working for Photos button, trying french ...")

    try:
        not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Photos')]"))).click()
        print("[+] French version found for accept button. Program continue...")
    except:
        print("[-] No french version working for Photos button. Program exit.")

    #scroll down n times
    #increase the range to sroll more
    n_scrolls = 1
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)


    # Download images

    images = driver.find_elements(By.TAG_NAME, 'img')
    images = [image.get_attribute("src") for image in images]

    # Create folder to save images
    nameFolderAndFiles = "targetFB"
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