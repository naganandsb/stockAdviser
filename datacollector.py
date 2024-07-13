# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:46:55 2024

@author: Dell
"""

import requests
import bs4
import json
import time
import numpy as np
import specialops as so
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class DataCollector:

    def login_and_get_html(website_url, username, password):
      driver = webdriver.Chrome()
      driver.get(website_url)

      username_field = driver.find_element(By.ID, "username")
      password_field = driver.find_element(By.ID, "password")
 
      username_field.send_keys(username)
      password_field.send_keys(password)
      password_field.submit()  # Submitting with password field is common

      time.sleep(5)  # Replace with a more robust waiting mechanism (e.g., waiting for element visibility)

      html_data = driver.page_source

      driver.quit()
    
      return html_data

    def getSector(self,soup):
        sector =soup.find("section",id="peers").find(class_="flex flex-space-between").a.text.strip()
        self.Data["Sector"] = sector

    def getTableData(self,soup,table_id):
        resp = soup.find(id=table_id,class_="card card-large").find("tbody").findAll("tr")
        
        for x in resp:
            tmp =[]
            for y in x.findAll("td"):
                tmp.append(y.text.strip())
            self.Data[table_id+"_"+ tmp[0].replace("\xa0+","")] = so.converToSuitable(tmp[1:])
    def __init__(self):
        self.Data = {}
        self.Company = None
    def scrapeDataURL(self,url):  
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Set headless mode
        driver = webdriver.Chrome(options=options)  # Replace with your preferred webdriver (e.g., Firefox)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "peers-table-placeholder")))

        content = driver.page_source  # Get the updated HTML content after JavaScript loads
        soup = BeautifulSoup(content, 'html.parser')
        self.Data["company_url"] = url
        self.Data["title"] = soup.title.string
        self.Data["breif"] = soup.find("div",class_="sub show-more-box about").text
        ratios = soup.find("div",class_="card card-large").findAll("li",class_="flex flex-space-between")
        for el in ratios:
            key = el.find("span",class_="name").text.strip()
            value =""
            no_of_eliments = el.findAll("span",class_="number")
            if len(no_of_eliments) > 1:
                for val in no_of_eliments:
                    value += val.text.strip()+"/"
                value = value[:-1]
            else:
                value = el.find("span",class_="number").text.strip()
            self.Data[key] = value
        self.Data["pros"] = [x.text.strip() for x in soup.find(class_="flex flex-column-mobile flex-gap-32").find(class_="pros").findAll("li")]

        self.Data["cons"] = [x.text.strip() for x in soup.find(class_="flex flex-column-mobile flex-gap-32").find(class_="cons").findAll("li")]
        
        self.getSector(soup)
        
        table_element = soup.find(id="peers-table-placeholder").find_all("a", href=True)
        peers ={}
        for i in table_element:
            peers[i.text] = i["href"]
        self.Data["peers"] = peers
        self.getTableData(soup,"quarters")
        self.getTableData(soup,"profit-loss")
        self.getTableData(soup,"balance-sheet")
        self.getTableData(soup,"cash-flow")
        self.getTableData(soup,"ratios")
        self.getTableData(soup,"shareholding")
        

        driver.quit()  # Close the browser window
        return self.Data
    
    def scrapeDataName(self,company):
        url  = f"https://www.screener.in/company/{company}/consolidated/"
        return self.scrapeDataURL(url)
    
def storeData(my_dict,**kw):
    if kw.get("store",True):
        with open('data.json', 'w') as f:
            json.dump(my_dict, f)

def loadData(**kw):
    if kw.get("fresh",False) == True:
        return []
    try:
        with open('data.json', 'r') as f:
            my_dict = json.load(f)
            return my_dict
    except:
        return []
def getCompaniesData(init,**kw):
    company_list =[init]
    
    companies_data = loadData(**kw)
       
    for i in company_list:
        url = "https://www.screener.in"+i
        if not len(companies_data) == 0:
            for company in companies_data:
                if(company["company_url"] == url):
                    url = None
                    break
            if url == None:
                continue
        try:
            c = DataCollector()
            data = c.scrapeDataURL(url)
        except Exception as e:
            print(e)
            continue
        companies_data.append(data)
        if kw.get("peers",False):
            for value in data["peers"].values():
                if not value in company_list:
                    company_list.append(value)
    
    storeData(companies_data,**kw)
    return companies_data
            
            