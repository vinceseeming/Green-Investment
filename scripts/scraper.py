#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
import os

import lxml
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import pandas as pd
from datetime import datetime 
import time


# In[ ]:


from basic_assistant import creat_company_url, get_request, main_url


# In[48]:


def scraper(cik):
    
    # find the 13f document webpage of a company/fund by a given CIK number
    
    time.sleep(0.15)
    
    response = get_request(create_company_url(cik))

    soup = BeautifulSoup(response.text, "lxml", parse_only=SoupStrainer(['a','span','input']))

    # find the 13F document tags of the company, and 
    # the tag contains the link to the detailed filing pages

    tags = soup.find_all('a', id="documentsbutton")

    # check if the company has 13f forms
    if len(tags)==0:
        #statement = "No 13f files found for this company"
        return False

    else:
        # retrieve name and cik information of the company
        company_name_text = soup.find('span', {'class': "companyName"}).get_text()
        company_name = re.sub(' CIK#.*$', '', company_name_text)
        company_cik_text = soup.find('input', {'name':'CIK'})
        company_cik = 'cik_number_' + company_cik_text.get('value')
        
        # scrape the detailed webpage of each 13f file
        for tag in tags:
            
            time.sleep(0.1)
            
            response_1 = get_request(main_url+tag['href'])
            soup_1 = BeautifulSoup(response_1.text, "lxml",parse_only=SoupStrainer(['div','strong','a']))
            
            # find the tag that contains the information table
            holding_tag = soup_1.find('a', href=lambda x: x and 'xslForm13F_X01'in x and not 'primary_doc' in x)
            
            # if no target table found, stop this round of loop
            if holding_tag is None:
                continue
            
            # retrieve the period of report of the 13f form
            time_tags = soup_1.find_all('div', class_="info")
            len_time = len(time_tags)
            if len_time < 5:
                continue
                
            period_of_report = time_tags[-2].get_text()

            # retrieve the file type of the 13f form, in case it is an amendment
            file_type_raw = soup_1.find('strong').get_text()
            file_type = file_type_raw.replace('/','-')
            

            try:
                # get the link to the information table page
                xml_url = holding_tag.get('href')
                
                # parse the information table page
                file_response = get_request(main_url+xml_url)
                
                HR_df = pd.read_html(file_response.text)
                HR_df = HR_df[-1]# the target table is the last one in the page
                # adjust the format of the dataframe
                HR_df = HR_df.iloc[2:]
                header_new = HR_df.iloc[0].tolist()
                header_new[3] = 'VALUE ' + header_new[3]
                header_new[4] = 'SHRS OR ' + header_new[4]
                header_new[5] = 'SH/' + header_new[5]
                header_new[6] = 'PUT/' + header_new[6]
                header_new[7] = 'INVESTMENT ' + header_new[7]
                header_new[8] = 'OTHER ' + header_new[8]
                #header_new[9] = 'VOTING AUTHORITY '+ header_new[9]
                #header_new[10]= 'VOTING AUTHORITY '+ header_new[10]
                #header_new[11]= 'VOTING AUTHORITY '+ header_new[11]
                HR_df.columns = header_new
                
                HR_df = HR_df.iloc[1:]
                
                HR_df['Company cik'] = company_cik
                HR_df['Company name'] = company_name
                HR_df['Period of report'] = period_of_report
                HR_df['File type'] = file_type
                
                # export the dataframe as a csv file to the data directory
                df_name = company_cik +'_'+ file_type +'_'+ period_of_report
                HR_df.to_csv(f"../data/13f/{df_name}.csv".format(df_name))

            except:
                print ('error')
                pass
        
        return True
          

