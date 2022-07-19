from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import glob

def move_to_download_folder(oldName, newName):
    got_file = False   
    seconds = 0
    ## Grab current file name.
    while (got_file == False):
        try: 
            f = open(oldName)
            got_file = True
        except FileNotFoundError:
            print ("File has not finished downloading")
            time.sleep(1)
            seconds += 1
            if (seconds > 30):
                print("Timeout, file is not downloading.")
                quit()
    
    ## Create new file name
    print (newName)
    os.rename(oldName, newName)

    return

##Mergent login password
with open('/equityreportcorrelator/password', 'r') as file:
    password = file.read().rstrip()

parent = '/equityreportcorrelator/Company Data/'
url = 'https://www.mergentonline.com/investextfullsearch.php'
companies = open('/equityreportcorrelator/companies')
#Creating the webdriver
s = Service("/usr/local/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/Users/arnavp4/Desktop/Capstone Project/User Data") #Path to chrome profile
options.page_load_strategy = 'normal'
options.add_argument('--enable-sync')
downloadpath = '/equityreportcorrelator/Individual Company Data/'
extension = ".xls"
fileprefix = 'searchresult'
oldPath = downloadpath + fileprefix + extension
prefs = {"download.default_directory" : downloadpath}
options.add_experimental_option("prefs",prefs)
options.add_experimental_option(
    'excludeSwitches',
    ['disable-sync'])
driver = webdriver.Chrome(options=options, service=s)
driver.get(url) #Opening the website
driver.find_element(By.XPATH, '//*[@id="loginarea"]/div[2]/div[2]/a').click() #Clicking on Login button
#Waiting for GT button to be pressed
print ("Click on Georgia Tech")
try:
    myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'cas')))
    print ("Page is ready!")
    time.sleep(2)
    #Logging into GT
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys("apatidar8")
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH,'//*[@id="login"]/section[4]/input[4]').click()
    time.sleep(6)
    driver.find_element(By.XPATH,'//*[@id="toptab"]/ul/li[15]/a').click() #Clicking on Investtext
    driver.find_element(By.XPATH, '//*[@id="search_topright"]/table/tbody/tr[1]/td[1]/a').click() 
    #Selecting Ticker from options
    select = Select(driver.find_element(By.XPATH, '//*[@id="search_criteria"]/table/tbody/tr/td[3]/select[1]'))
    select.select_by_visible_text('Ticker')
    companynumber = 0
    for company in companies:
        newPath = downloadpath + company.strip() + extension
        #Inputting company name into text box
        driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[4]/input').clear()
        driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[4]/input').send_keys(company)
        time.sleep(2)
        #Downloading spreadsheet
        driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[6]/input').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[8]/a[2]').click()
        recievedTicker = str(driver.find_element(By.XPATH, '//*[@id="tab1"]/b[1]').text)
        wrongInput = True
        while(wrongInput):
            if (recievedTicker.strip()!= company.strip()):
                print('Ticker was not inputted properly into the text box.')
                driver.back()
                driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[4]/input').clear()
                driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[4]/input').send_keys(company)
                time.sleep(2)
                #Downloading spreadsheet
                driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[6]/input').click()
                time.sleep(2)
                driver.find_element(By.XPATH,'//*[@id="search_criteria"]/table/tbody/tr/td[8]/a[2]').click()
                recievedTicker = str(driver.find_element(By.XPATH, '//*[@id="tab1"]/b[1]').text)
            else:
                wrongInput = False
        driver.find_element(By.XPATH,'//*[@id="excellinkid"]').click()
        move_to_download_folder(oldPath, newPath)
        driver.back()
        time.sleep(3)
except TimeoutException:
    print ("Loading took too much time!")


