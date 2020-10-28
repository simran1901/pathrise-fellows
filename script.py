import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import argparse

class ConnectEndorse():
    def __init__(self):
        pass

    def clickButtonByText(self,txt):
        connect_button = self.browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
        if connect_button:
            connect_button[0].click()

    def expandShowMore(self):
        self.browser.find_elements_by_xpath('//button[@class= ')[0].click()


    def endorse(self):
        self.scrollUntil("Skills & Endorsements")
        
        # Open skills and endorsements, show more
        elem = self.getElementByTxt("Skills & Endorsements")
        self.scrollTo(elem[0])  
        self.browser.implicitly_wait(3)

        # This opens the 'show more' right after skills and endorsements
        elem = self.getElementByTxt("Show more")
        self.scrollTo(elem[0])
        elem[0].click()

        res = self.browser.find_elements_by_xpath(\
                "//button[@aria-label[contains(.,'Endorse')]"+\
                " and @aria-pressed[contains(.,'false')] ]")    
        for r in res[:10]:
            try:
                self.scrollTo(r)        
                r.click()
                self.browser.implicitly_wait(5)
                self.getElementByTxt("Highly skilled")
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
            except:
                print("exception occured in endorsement")
            # break
            pass
        self.scrollDown()
        pass
    
    def scrollUntil(self,txt):
        maxScroll = 15
        keepScrolling = True
        count = 0
        while keepScrolling:
            if count > maxScroll:
                return False
            if self.containsTxt(txt):
                keepScrolling = False
                return True
            self.scrollDown()
            count += 1    
        

    
    def scrollDown(self):
        body = self.browser.find_element_by_xpath('/html/body')
        ActionChains(self.browser).send_keys(Keys.PAGE_DOWN).perform()

    def scrollDownBottom(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def scrollTo(self,elem):
        actions = ActionChains(self.browser)
        actions.move_to_element(elem).perform()

    def containsTxt(self,txt):
        result = self.browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
        return bool(result)

    def getElementByTxt(self,txt):
        result = self.browser.find_elements_by_xpath("//*[text()='{}']".format(txt))
        return result


    def main(self,authPath="resources/auth.txt",fellowPath="resources/fellows.csv"):
        # todo: have assert chromedriver available
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument('--no-sandbox')
        opt.add_argument("--disable-extensions")

        # to  manage permssions un-comment these lines and adjust them accordingly.
        # opt.add_experimental_option("prefs", {
        #                                 "profile.default_content_setting_values.media_stream_mic": 1,
        #                                 "profile.default_content_setting_values.media_stream_camera": 1,
        #                                 "profile.default_content_setting_values.geolocation": 2,
        #                                 "profile.default_content_setting_values.notifications": 2,
        # })
        
        self.browser = webdriver.Chrome(options=opt, executable_path='/usr/local/bin/chromedriver')
        self.browser.get('https://www.linkedin.com/login?fromSignIn=true"+\
                            "&trk=guest_homepage-basic_nav-header-signin')
        # todo: change this to be args passed in
        f = open(authPath,"r")
        userStr = f.readline()
        pwStr = f.readline()
        username = self.browser.find_element_by_id('username')
        pw = self.browser.find_element_by_id('password')
        username.send_keys(userStr)
        pw.send_keys(pwStr)
        df = pd.read_csv(fellowPath)
        count = 0
        for idx,row in df.iterrows():
            # This loop iterates through the CSV, checking
            # condition of friendship of user, and either connects or endorses
            if count > 3: break # for debugging
            # load user profile
            url = row['LinkedIn']
            try:
                self.browser.get(url)
                self.browser.implicitly_wait(2)
                if self.containsTxt("Connect"):
                    print("sending friend request: {} {}".format(row['First name'],row['Last Name']))
                    self.clickButtonByText("Connect")
                    self.clickButtonByText("Send now")        
                    pass
                # check if friendship request pending
                elif self.containsTxt("Pending"):
                    print("pending friend request: {} {}".format(row['First name'],row['Last Name']))
                    pass 
                elif self.containsTxt("1st"):
                    # check if friendship confirmed
                    self.endorse()
                    pass
                pass
            except:
                print("Invalid URL for {} {}".format(row['First name'],row['Last Name']))
            pass


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("loginPath", help="path to login text file")
    parser.add_argument("fellowsCsvPath", help="path to fellows csv file")    
    args = parser.parse_args()    
    p = ConnectEndorse()
    p.main(args.loginPath,args.fellowsCsvPath)
    pass
