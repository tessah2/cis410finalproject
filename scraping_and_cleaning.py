#!/usr/bin/env python
# coding: utf-8

# TO RUN IN COMMAND LINE:
# python3 data_cleaning.py
# OR (depending on how you have python set up)
# python data_cleaning.py

# import necessary libraries.  you may need to install them as well.
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib

import numpy as np
import math
import pandas as pd


###################
###### Scrape Stanford Encyclopedia of Philosophy page urls

options = Options()
options.headless = True
browser = webdriver.Chrome('./chromedriver',options=options)


def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') 
    return soup

#tidies extracted text 
def process_entry(entry):
    entry = entry.encode('ascii',errors='ignore').decode('utf-8')      
    entry = re.sub('\s+',' ',entry)       
    return entry



# extracts all entry page urls from the Stanford Encyclopedia of Philosophy Table of Contents Page
def scrape_dir_page(dir_url,browser):
    print ('-'*20,'Scraping directory page','-'*20)
    encyclo_links = [] 
    encyclo_base_url = 'https://plato.stanford.edu/'
    substring = 'entries'
    #execute js on webpage to load encyclopedia listings on webpage and get ready to parse the loaded HTML
    soup = get_js_soup(dir_url,browser)     
    for link_holder in soup.find_all('a'): 
        rel_link = link_holder.get('href') #get url
        if isinstance(rel_link, str) is True and substring in rel_link:
            encyclo_links.append(encyclo_base_url+rel_link) 
    print ('-'*20,'Found {} table of contents urls'.format(len(encyclo_links)),'-'*20)
    return encyclo_links


dir_url = 'https://plato.stanford.edu/contents.html'
encyclo_links = scrape_dir_page(dir_url,browser)


# for writing data to files
def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')



# write Stanford Encyclopedia of Philosophy entry urls to .txt file
entry_urls_file = 'data/encyclo_urls.txt'
write_lst(encyclo_links,entry_urls_file)



#############################################
#### url and essay keyword data cleaning


# read in data
urls=pd.read_csv("data/encyclo_urls.txt",delimiter="\t",header=None)

urls = pd.DataFrame(urls)

# split urls to extract only the entry name part as keywords
newurls = urls[0].str.split("entries/", n = 1, expand = True)


# clean up entry name part of urls to eliminate dashes and slashes
cols_to_check = [1]
newurls[cols_to_check] = newurls[cols_to_check].replace({'/':''}, regex=True)
newurls[cols_to_check] = newurls[cols_to_check].replace({'-':' '}, regex=True)
#print(newurls)

# eliminate part of url to keep only the entry page name
newurls = newurls[[1]]

# add full urls to the entry page name
newurls['urls'] = urls
#print(newurls)

# save Stanford Encyclopedia of Philosophy entry page names and their accompanying urls to a .csv file.
#newurls = newurls.rename(columns={1: 'entryname'}, inplace=True)
newurls.to_csv('data/encyclo_titles.csv', sep='\t')


entrynames = newurls[[1]]
# convert dataframe to list of lists
entrynames = entrynames.values.tolist()
# flatten list of lists to list
entrynameslist = [item for sublist in entrynames for item in sublist]
# convert list to string
entrynamesstring = ' '.join([str(elem) for elem in entrynames])

############################
# Create proper noun list from a philosophy essay (e.g., nagel_bat.txt)
# to see if there are any relevant Stanford Encyclopedia of Philosophy Entries

# read in list of Stanford Encyclopedia of Philosophy page titles
df=pd.read_csv("data/encyclo_titles.csv",delimiter="\t",header=None)

# read in philosophy document
# EDIT file name here for a different philosophy essay document in the data folder
f = open('data/nagel_bat.txt')
with open('data/nagel_bat.txt', 'r') as file:
    data = file.read().replace('\n', '')


# create list of words
words = []
for line in f:
    for word in line.split():
        words.append(word)


# clean up list of words
# remove all special characters
words = [re.sub(r'\W', '', x) for x in words]
# make all words lowercase
words = [x.lower() for x in words]
# remove all strings that contain a number
words = [x for x in words if not any(c.isdigit() for c in x)]
#print(words[1:100])


# create list of unique words
vocabulary = []
unique_words = set(words)
for word in unique_words:
    vocabulary.append(word)

#print(vocabulary[1:100])


#import gensim
#from gensim.summarization.summarizer import summarize
#print(summarize(data))


# import spacy for pos tagging of philosophy document
import spacy
nlp = spacy.load("en_core_web_sm")

import en_core_web_sm
nlp = en_core_web_sm.load()

doc = nlp(data)

#print("Proper Noun:", [token.text for token in doc if token.pos_ == "PROPN"])
propernouns = [token.text for token in doc if token.pos_ == "PROPN"]

propernouns = [re.sub(r'\W', '', x) for x in propernouns]
propernouns = [x for x in propernouns if not any(c.isdigit() for c in x)]
propernouns = [x.lower() for x in propernouns]
#print(propernouns)


# create unique list of proper nouns
propnouns = [] 
unique_words = set(propernouns)
for word in unique_words:
    propnouns.append(word)
#print(propnouns)


#from spacy import displacy
#about_interest_text = data
#about_interest_doc = nlp(about_interest_text)
#displacy.serve(about_interest_doc, style='dep')


# output intersection of words in Stanford Encyclopedia of philosophy entry names
# and proper nouns in the chosen philosophy essay (e.g., nagel_bat.txt)

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

lst1 = propnouns
lst2 = entrynameslist

# intersection results
sep_recs = intersection(lst1, lst2)
#print(sep_recs)
#convert to dataframe

# rename url column within df
#sep_recs = sep_recs.rename(columns={1: 'entryname'}, inplace=True)
#print(sep_recs)

#sep_recs = pd.DataFrame(sep_recs)
#sep_recs = sep_recs.rename(columns={0: 'entryname'}, inplace=True)

#print(sep_recs)

#sep_recs.to_csv('data/sep_recs.csv', sep='\t')

#merged_inner = sep_recs.merge(newurls, on='entryname')
#print(merged_inner)

# for writing data to files
def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')

# write Stanford Encyclopedia of Philosophy entry name recommendations to .txt file
sep_recs_file = 'data/sep_recs.txt'
write_lst(sep_recs,sep_recs_file)
