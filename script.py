from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def clickButtonByText(txt):
    connect_button = browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
    if connect_button:
        connect_button[0].click()

# [contains(.,'pv-profile-section__card-action-bar pv-skills-section__additional-skills')]      
def expandShowMore():
    browser.find_elements_by_xpath('//button[@class= ')[0].click()

# browser.find_elements_by_xpath("//html").click();    
def endorse():
    res = browser.find_elements_by_xpath("//button[@aria-label[contains(.,'Endorse')]]")
    if res:
        idx = 0
        while idx < 8 and idx < len(res):
            res[idx].click()
            browser.implicitly_wait(3000)
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            idx+=1
            pass
        pass
    pass


browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')


## Type this in
f = open("resources/auth.txt","r")
userStr = f.readline()
pwStr = f.readline()

username = browser.find_element_by_id('username')
pw = browser.find_element_by_id('password')

username.send_keys(userStr)
pw.send_keys(pwStr)
pw.send_keys(Keys.ENTER)

import pandas as pd
df = pd.read_csv('fellows.csv')

count = 0
for idx,row in df.iterrows():
    # check if friend request not sent
    # check if friendship request pending
    # check if friendship confirmed
    if count > 3: break # for debugging
    print(row['LinkedIn'])
    browser.get(row['LinkedIn'])
    print("waiting")    
    browser.implicitly_wait(3000)    
    # browser.get('https://www.linkedin.com/in/davidngetich/')
    try:
        print("clicking")
        clickButtonByText("Connect")
        clickButtonByText("Send now")
        browser.implicitly_wait(5000)
        print("done")
    except e:
        pass
    count += 1
