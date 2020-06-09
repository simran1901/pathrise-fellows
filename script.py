import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading

def clickButtonByText(txt):
    connect_button = browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
    if connect_button:
        connect_button[0].click()

def expandShowMore():
    browser.find_elements_by_xpath('//button[@class= ')[0].click()


def endorse():
    # scroll down pg dwn to load skills sec.
    for i in range(3):
        scrollDown()
        pass
    browser.implicitly_wait(3)            
    elem = getElementByTxt("Skills & Endorsements")
    scrollTo(elem[0])  
    browser.implicitly_wait(3)      
    elem = getElementByTxt("Show more")
    scrollTo(elem[0])
    elem[0].click()
    browser.implicitly_wait(3)    
    res = browser.find_elements_by_xpath("//button[@aria-label[contains(.,'Endorse')]]")
    for r in res[:5]:
        scrollTo(r)        
        r.click()
        browser.implicitly_wait(5)
        getElementByTxt("Highly skilled")
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        # break
        pass
    scrollDown()
    pass

def scrollDown():
    body = browser.find_element_by_xpath('/html/body')
    # body.click()
    ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()

def scrollDownBottom():
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

def scrollTo(elem):
    actions = ActionChains(browser)
    actions.move_to_element(elem).perform()

def containsTxt(txt):
    result = browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
    return bool(result)

def getElementByTxt(txt):
    result = browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
    return result

# todo: have assert chromedriver available
browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

# todo: change this to be args passed in
f = open("resources/auth.txt","r")
userStr = f.readline()
pwStr = f.readline()

username = browser.find_element_by_id('username')
pw = browser.find_element_by_id('password')

username.send_keys(userStr)
pw.send_keys(pwStr)


df = pd.read_csv('resources/fellows.csv')
count = 0
for idx,row in df.iterrows():
    if count > 3: break # for debugging
    
    # load user profile
    url = row['LinkedIn']
    browser.get(url)
    browser.implicitly_wait(3)
    
    # check if friend request not sent
    if containsTxt("Connect"):
        print("sending friend request: {} {}".format(row['First name'],row['Last Name']))
        clickButtonByText("Connect")
        # clickButtonByText("Send now")        
        pass
    # check if friendship request pending
    elif containsTxt("Pending"):
        print("pending friend request: {} {}".format(row['First name'],row['Last Name']))
        pass
    else: 
        # check if friendship confirmed
        endorse()
        pass

