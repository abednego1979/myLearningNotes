# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import time
import re


class myWebDriver():
    
    def __init__(self, dbg=False):
        self.timeout=10
        self.dbg=dbg
        self.driver=webdriver.Ie(executable_path='C:\\Program Files\\Internet Explorer\\IEDriverServer.exe')
        self.driver.set_page_load_timeout(self.timeout)
        self.driver.set_script_timeout(self.timeout)
        self.driver.maximize_window()
        return

    def getUrl(self, url, keepOpen=False):
        out=""
        try:
            try:
                self.driver.get(url)
            except TimeoutException:
                if self.dbg:
                    print ('time out after %d seconds when loading page' % self.timeout)
                self.driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
            
            if self.dbg:
                print ("当前URL：", self.driver.current_url)
            out=self.driver.page_source
        except:
            if self.dbg:
                print ("Get %s Fail" % url)
        finally:
            if not keepOpen:
                self.driver.quit()
            return out
        
    def close(self):
        try:
            self.driver.quit()
        except:
            pass
        return
    
    def clickSelect(self, XPath=""):
        tryNum=3
        while True:
            if not tryNum:
                break
            tryNum-=1
            try:
                select=self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/ul/li/div/i')
                break
            except:
                time.sleep(2)
                continue
        if not tryNum:
            return False
        
        select.click()
        time.sleep(2)        
        
        return True
    def needLogin(self):
        time.sleep(2)
        login=self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div[3]/div/div/div/div/span')
        return login.is_displayed()
    
    def login(self):
        time.sleep(2)
        login=self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div[3]/div/div/div/div/span').click()
        time.sleep(3)
        
        self.driver.switch_to.frame(0)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
        time.sleep(1)
        
        user=self.driver.find_element_by_id('u').click()
        time.sleep(1)
        
        user=self.driver.find_element_by_id('p').click()
        time.sleep(1)        
        
        return

r'''
baseUrl='http://qimila.vip'


d=myWebDriver(dbg=False)
out = d.getUrl(baseUrl)

soup = BeautifulSoup(out, "lxml")
links=[]
try:
    main_link = soup.find("div",attrs={"id":"portal_block_24_content"}).find("div",attrs={"class":"module cl xl xl1"}).find("ul").findAll("li")
    for item in main_link:
        try:
            temp_title=item.find("a").attrs['title']
            temp_url=item.find("a").attrs['href']
            temp_url=baseUrl+"/"+temp_url if not temp_url.startswith("http") else temp_url
            links.append([temp_title, temp_url])
        except:
            print ("Something ERROR!")
            continue
except:
    pass

for item in links:
    print ("title:", item[0])
    print ("access:", item[1])    
    d=myWebDriver()
    out = d.getUrl(item[1])
    
    soup = BeautifulSoup(out, "lxml")
    for weiyunLink in soup.findAll("a"):
        if ('href' in weiyunLink.attrs.keys()) and ("share.weiyun.com" in weiyunLink.attrs['href']):
            print (weiyunLink.attrs['href'])
'''

baseUrl="https://share.weiyun.com/5HGG5Rm"

d=myWebDriver()
out = d.getUrl(baseUrl, keepOpen=True)

if d.needLogin():
    print ("Need to login")
    d.login()
else:
    print ("Need not to login")
d.clickSelect()
d.close()

print (".")
