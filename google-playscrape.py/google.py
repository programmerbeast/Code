from google_play_scraper import app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import re
import time



#####
#maak een list met alle links die worden verkregen uit de website, ze zijn in de tr
#eze list wordt doorgeloopt en op geklikt
#Daarna wordt er naar een email gezocht doormiddel van de email zoek functie
####







#####
def main():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.appbrain.com/stats/google-play-rankings#categories")
    scrape(driver)
    show_results()
    driver.quit()

def scrape(driver):
    listOfElements = driver.find_elements(By.XPATH,(".//td[@class='ranking-app-cell']"))

    driver.implicitly_wait(5000)
    global find_emails 
    find_emails = []
    
    for i in range(len(listOfElements)):
        try:
            listOfElements = driver.find_elements(By.XPATH,(".//td[@class='ranking-app-cell']"))
            listOfElements[i].click()                                               
            get_url = driver.current_url                                 
            source = requests.get(get_url)
            soup = BeautifulSoup(source.text, 'lxml')
                    # Look for emails on the website
   
            find_emails.append(soup.body.findAll(text=re.compile('@+[a-zA-Z0-9.-]+.(com|net|co|org|us|info|biz|me|nl)'))) #instead of re.findall
            driver.get("https://www.appbrain.com/stats/google-play-rankings#categories")
            time.sleep(3)
        except:
            print(find_emails[0])
            break



def show_results():
    print(find_emails)



    
main()



result = app(
    'com.nianticlabs.pokemongo',
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)




    #pattern = "(https://|http://)+(|www.)+[a-zA-Z0-9.-]+.(com|net|co|org|us|info|biz|me|nl)+(|/)"
    #p = re.compile(pattern) 
    #driver.navigate().back()


      #  print('false')

    #parentElement = driver.find_elements(By.CLASS_NAME,"yuRUbf")
    #for element in parentElement:
      #elementList = element.find_element(By.TAG_NAME,"a")
      #link = elementList.get_attribute("href")
      #print(link)
      #validurl(link)

    #for element in listOfElements:
    #n = 0

   # driver.get("https://www.appbrain.com/stats/google-play-rankings#categories")
    
#wait = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CLASS_NAME, "ULeU3b")))
    #source = requests.get("https://play.google.com/store/apps/collection/topselling_free?clp=ChcKFQoPdG9wc2VsbGluZ19mcmVlEAcYAw%3D%3D:S:ANO1ljLwMrI&gsr=ChkKFwoVCg90b3BzZWxsaW5nX2ZyZWUQBxgD:S:ANO1ljIxP20&hl=en&gl=US")
    #soup = BeautifulSoup(source.text, 'lxml')
                    # Look for emails on the website
    #find_emails = soup.body.findAll(text=re.compile('@')) #instead of re.findall
    #print(soup)
    #if driver.find_element(By.CLASS_NAME, "ULeU3b") == True:
      #  print('hallo mohamed')
      #  print('hallo mohamed')
    #l = listOfElements[start_count[n]]                                                                             
    #l.get_attribute('innerHTML')
                                                            
    #print(l.get_attribute('innerHTML'))
    #print(element.get_attribute('innerHTML'))