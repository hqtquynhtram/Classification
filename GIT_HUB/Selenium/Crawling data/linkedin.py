# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 23:13:47 2019

@author: defaultuser0
"""

dir="C:\\Users\\defaultuser0.LAPTOP-6F0LJR1V\\Selenium"
import os
os.chdir(dir)

import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv
from selenium.webdriver.support.ui import Select
import pandas as pd


def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer=csv.writer(open(parameters.file_name, 'w'))
writer.writerow(['Job Title','Company Name','Time','Applicants','Place','Job Description','Skill','Url'])

driver=webdriver.Chrome('D:/chromedriver')
driver.get('https://www.linkedin.com/')

username=driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password=driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button=driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

driver.get('http://google.com')
sleep(2)

search_query=driver.find_element_by_name('q')
search_query.send_keys(parameters.search)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

links=driver.find_elements_by_xpath('//*[@class="r"]/a')
link= links[0].get_attribute("href")
sleep(3)

driver.get(link)
sleep(10)

#Make all job position is visible

element=driver.find_elements_by_xpath('//*[@class="job-card-search__title artdeco-entity-lockup__title ember-view"]//a')

element[1].send_keys(Keys.END)
sleep(10)
element[1].send_keys(Keys.HOME)
sleep(10)

url_link=driver.find_elements_by_xpath('//*[@class="job-card-search__title artdeco-entity-lockup__title ember-view"]//a')
print(len(url_link))
job_url_link=[content.get_attribute("href") for content in url_link]
full_list=[]
full_list.append(job_url_link)


def find_number_of_next_page():
    next_page=None
    next_button=driver.find_elements_by_xpath('//*[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]//span')
    button_selected=driver.find_elements_by_xpath('//*[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number active selected"]/span')
    for i in range(len(next_button)):
        if button_selected[0].text==next_button[i].text:
            next_page=next_button[i+1]
        else:
            pass
    return(next_page)
    

from selenium.common.exceptions import NoSuchElementException        

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
username='//*[@class="t-16 t-black t-bold pt2 pb2"]'        

last_page=driver.find_elements_by_xpath('//*[@class="artdeco-pagination__pages artdeco-pagination__pages--number"]//span')[-1].text

#Next pages
for i in range(int(last_page)-1):
    url_list= []
    company_section= []
    next_page=find_number_of_next_page()
    next_page.click()
    sleep(10)
    element=driver.find_elements_by_xpath('//*[@class="job-card-search__title artdeco-entity-lockup__title ember-view"]//a')
    element[1].send_keys(Keys.END)
    sleep(5)
    element[1].send_keys(Keys.HOME)
    sleep(5)
    company_section=driver.find_elements_by_xpath('//*[@class="job-card-search__title artdeco-entity-lockup__title ember-view"]//a')
    url_list=[content.get_attribute("href") for content in company_section]
    full_list.append(url_list)
        

#Save url list as excel file    
url_list_df=pd.Series(full_list)
url_list_df.to_excel('Seattle.xlsx')

    



#Crawl content in each url
list_all=pd.read_excel('Seattle.xlsx')

username='//*[@class="t-16 t-black t-bold pt2 pb2"]'        

for i in range(len(list_all)):

    for link in eval(list_all.iloc[i+13,1]):
        driver.get(link)
        sleep(5)
    
        sel=Selector(text=driver.page_source)
        
        job_title=sel.xpath('//*[@class="jobs-top-card__job-title t-24"]/text()').extract_first()
        if job_title:
            job_title=job_title.strip()
    
        
        company_name=sel.xpath('//*[@class="jobs-top-card__company-url ember-view"]/text()').extract_first()
        if company_name:
            company_name=str(company_name).strip()
        
        posting_time=sel.xpath('//*[@class="mt1 full-width flex-grow-1 t-14 t-black--light"]/span/text()').extract()
        if posting_time:
            posting_time=str(posting_time).strip()
            
        
        applicants=sel.xpath('//*[@class="jobs-top-card__bullet inline-flex align-items-center mr1"]/span/text()').extract()
        if applicants:
            applicants=str(applicants).strip()    
        
        place=sel.xpath('//*[@class="jobs-top-card__bullet"]/text()').extract_first()
        if place:
            place=str(place).strip()
    
        description=sel.xpath('//*[@id="job-details"]//text()').extract()
        description= [x.strip('\n') for x in description]
        description=str(description)[1:-1]
        description=description.strip()
        
    
        skill=sel.xpath('//*[@class="jobs-ppc-criteria__value t-14 t-black t-normal ml2 block"]//text()').extract()
        skill=str(skill).strip()
    
        url=driver.current_url
    
        job_title=validate_field(job_title)
        company_name=validate_field(company_name)
        posting_time=validate_field(posting_time)
        applicants=validate_field(applicants)
        place=validate_field(place)
        description=validate_field(description)
        skill=validate_field(skill)
        url =validate_field(url)
    
        print('Job Titile: '+job_title)
        print('Company Name: '+ company_name)
        print('Time: '+ posting_time)
        print('Applicant: '+ applicants) 
        print('Place: '+place)
        print('Job Description: '+ description)
        print('Skill: '+ skill)
        print('Url: '+url)
    
        writer.writerow([job_title.encode('utf-8'),
                        company_name.encode('utf-8'),
                        posting_time.encode('utf-8'),
                        applicants.encode('utf-8'),
                        place.encode('utf-8'),
                        description.encode('utf-8'),
                        skill.encode('utf-8'),
                        url.encode('utf-8')])

driver.quit()




