#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

def create_company_url(cik):
    'Returns url of the page of company filings given a CIK.'
    return f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=13f&dateb=20210331&owner=exclude&count=40&search_text='

headers = {"User-Agent":"yiming.shi@student.kuleuven.be",
           "Accept-Encoding":"gzip, deflate",
           "Host":"www.sec.gov"}

def get_request(url):
    'Returns result of a http request to url.'
    return requests.get(url, headers=headers)

main_url = 'https://www.sec.gov'

