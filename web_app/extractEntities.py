
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:21:34 2019

@author: prach
"""

import re

def extract_name(resume):
   
   
    nlp = en_core_web_sm.load()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(resume)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            print(ent.text)
            break 
    return ent.text                  


def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers if len(number) >9]


def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


