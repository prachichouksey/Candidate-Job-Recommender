# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:21:34 2019

@author: prach
"""

import bs4
import numpy
import pandas
import re
import requests
import datetime

input_job = "Data Scientist"
input_quote = False 
input_city = "San Jose" 
input_state = "CA"
sign = "+"
BASE_URL_indeed =  'https://www.indeed.com/' 

def transform(input,sign, quote = False):
    syntax = input.replace(" ", sign)
    if quote == True:
        syntax = ''.join(['"', syntax, '"'])
    return(syntax)


if not input_city: 
    url_indeed_list = [ BASE_URL_indeed, '/jobs?q=', transform(input_job, sign, input_quote),
                    '&l=', input_state]
    url_indeed = ''.join(url_indeed_list)
else: 
    url_indeed_list = [ BASE_URL_indeed, '/jobs?q=', transform(input_job, sign, input_quote),
                    '&l=', transform(input_city, sign), '%2C+', input_state]
    url_indeed = ''.join(url_indeed_list)
print(url_indeed)


rawcode_indeed = requests.get(url_indeed)

soup_indeed = bs4.BeautifulSoup(rawcode_indeed.text, "lxml")


num_total_indeed = soup_indeed.find(
                        id = 'searchCount').contents[0].split()[-2]
print("total results:")
print(soup_indeed.find(id = 'searchCount').contents[0])
print(soup_indeed.find(id = 'searchCount').contents[0].split()[-2])
num_total_indeed = re.sub("[^0-9]","", num_total_indeed) 
num_total_indeed = int(num_total_indeed)
print(num_total_indeed)


num_pages_indeed = int(numpy.ceil(num_total_indeed/10.0))
print(num_pages_indeed)

job_df_indeed = pandas.DataFrame()
now = datetime.datetime.now()
now_str = now.strftime("%m/%d/%Y")
now_str_name=now.strftime('%m%d%Y')


for i in range(1, num_pages_indeed+1):
    
    url = ''.join([url_indeed, '&start=', str(i*10)])
    print(url)

    
    rawcode = requests.get(url)
    soup = bs4.BeautifulSoup(rawcode.text, "lxml")

    
    divs = soup.findAll("div")
    job_divs = [jp for jp in divs if not jp.get('class') is None
                    and 'row' in jp.get('class')]
    
    for job in job_divs:
        try:
            
            id = job.get('data-jk', None)
            
            link = BASE_URL_indeed + '/rc/clk?jk=' + id
            
            title = job.find('a', attrs={'data-tn-element': 'jobTitle'}).attrs['title']
            
            company = job.find('span', {'class': 'company'}).text.strip()
            
            location = job.find('span', {'class': 'location'}).text.strip()
        except:
            continue

        job_df_indeed = job_df_indeed.append({'job_title': title,
                                'job_id': id,
                                'job_company': company,
                                'date': now_str,
                                'from':'Indeed',
                                'job_location':location,
                                'job_link':link},ignore_index=True)
cols=['from','date','job_id','job_title','job_company','job_location','job_link']
job_df_indeed = job_df_indeed[cols]
print(job_df_indeed.shape)


job_df_indeed = job_df_indeed.drop_duplicates(['job_link'], keep='first')


print(job_df_indeed.shape)


path = 'job_indeed_scrape_' + now_str_name + '.csv'
job_df_indeed.to_csv(path)

import bs4
import numpy
import pandas
import re
import requests
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')

job_df_indeed = pandas.DataFrame.from_csv(path)


type = ['Full-Time', 'Full Time', 'Part-Time', 'Part Time', 'Contract', 'Contractor']
type_lower = [s.lower() for s in type] 

type_map = pandas.DataFrame({'raw':type, 'lower':type_lower}) 
type_map['raw'] = ["Full-Time", "Full-Time", 'Part-Time', 'Part-Time', "Contract", 'Contract'] 
type_dic = list(type_map.set_index('lower').to_dict().values()).pop() 

skills = ['R', 'Shiny', 'RStudio', 'Markdown', 'Latex', 'SparkR', 'D3', 'D3.js',
            'Unix', 'Linux', 'MySQL', 'Microsoft SQL server', 'SQL',
            'Python', 'SPSS', 'SAS', 'C++', 'C', 'C#','Matlab','Java',
            'JavaScript', 'HTML', 'HTML5', 'CSS', 'CSS3','PHP', 'Excel', 'Tableau',
            'AWS', 'Amazon Web Services ','Google Cloud Platform', 'GCP',
            'Microsoft Azure', 'Azure', 'Hadoop', 'Pig', 'Spark', 'ZooKeeper',
            'MapReduce', 'Map Reduce','Shark', 'Hive','Oozie', 'Flume', 'HBase', 'Cassandra',
            'NoSQL', 'MongoDB', 'GIS', 'Haskell', 'Scala', 'Ruby','Perl',
            'Mahout', 'Stata']
skills_lower = [s.lower() for s in skills]
skills_map = pandas.DataFrame({'raw':skills, 'lower':skills_lower})
skills_map['raw'] = ['R', 'Shiny', 'RStudio', 'Markdown', 'Latex', 'SparkR', 'D3', 'D3',
            'Unix', 'Linux', 'MySQL', 'Microsoft SQL server', 'SQL',
            'Python', 'SPSS', 'SAS', 'C++', 'C', 'C#','Matlab','Java',
            'JavaScript', 'HTML', 'HTML', 'CSS', 'CSS','PHP', 'Excel', 'Tableau',
            'AWS', 'AWS','GCP', 'GCP',
            'Azure', 'Azure', 'Hadoop', 'Pig', 'Spark', 'ZooKeeper',
            'MapReduce', 'MapReduce','Shark', 'Hive','Oozie', 'Flume', 'HBase', 'Cassandra',
            'NoSQL', 'MongoDB', 'GIS', 'Haskell', 'Scala', 'Ruby','Perl',
            'Mahout', 'Stata']
skills_dic = list(skills_map.set_index('lower').to_dict().values()).pop()

edu = ['Bachelor', "Bachelor's", 'BS', 'B.S', 'B.S.', 'Master', "Master's", 'Masters', 'M.S.', 'M.S', 'MS',
        'PhD', 'Ph.D.', "PhD's", 'MBA']
edu_lower = [s.lower() for s in edu]
edu_map = pandas.DataFrame({'raw':edu, 'lower':edu_lower})
edu_map['raw'] = ['BS', "BS", 'BS', "BS", 'BS', 'MS', "MS", 'MS', 'MS', 'MS', 'MS',
        'PhD', 'PhD', "PhD", 'MBA'] 
edu_dic = list(edu_map.set_index('lower').to_dict().values()).pop()

major = ['Computer Science', 'Statistics', 'Mathematics', 'Math','Physics',
            'Machine Learning','Economics','Software Engineering', 'Engineering',
            'Information System', 'Quantitative Finance', 'Artificial Intelligence',
            'Biostatistics', 'Bioinformatics', 'Quantitative']
major_lower = [s.lower() for s in major]
major_map = pandas.DataFrame({'raw':major, 'lower':major_lower})
major_map['raw'] = ['Computer Science', 'Statistics', 'Math', 'Math','Physics',
            'Machine Learning','Economics','Software Engineering', 'Engineering',
            'Information System', 'Quantitative Finance', 'Artificial Intelligence',
            'Biostatistics', 'Bioinformatics', 'Quantitative']
major_dic = list(major_map.set_index('lower').to_dict().values()).pop()

keywords = ['Web Analytics', 'Regression', 'Classification', 'User Experience', 'Big Data',
            'Streaming Data', 'Real-Time', 'Real Time', 'Time Series']
keywords_lower = [s.lower() for s in keywords]
keywords_map = pandas.DataFrame({'raw':keywords, 'lower':keywords_lower})
keywords_map['raw'] = ['Web Analytics', 'Regression', 'Classification', 'User Experience', 'Big Data',
            'Streaming Data', 'Real Time', 'Real Time', 'Time Series']
keywords_dic = list(keywords_map.set_index('lower').to_dict().values()).pop()


list_type = []
list_skill = []
list_text = []
list_edu = []
list_major = []
list_keywords = []

for i in range(len(job_df_indeed)):
    
    required_type= []
    required_skills = []
    required_edu = []
    required_major = []
    required_keywords = []

    try:
        
        job_page = requests.get(job_df_indeed.iloc[i, 6])
        
        soup = bs4.BeautifulSoup(job_page.text, "lxml")

        
        for elem in soup.findAll(['script','style','head','title','[document]']):
            elem.extract()
        
        texts = soup.getText(separator=' ').lower()

        
        string = re.sub(r'[\n\r\t]', ' ', texts) 
        string = re.sub(r'\,', ' ', string) 
        string = re.sub('/', ' ', string) 
        string = re.sub(r'\(', ' ', string) 
        string = re.sub(r'\)', ' ', string) 
        string = re.sub(' +',' ',string) 
        string = re.sub(r'r\s&\sd', ' ', string) 
        string = re.sub(r'r&d', ' ', string) 
        string = re.sub('\.\s+', ' ', string) 

        
        for typ in type_lower :
            if any(x in typ for x in ['+', '#', '.']):
                typp = re.escape(typ) 
            else:
                typp = typ
            result = re.search(r'(?:^|(?<=\s))' + typp + r'(?=\s|$)', string) 
            if result:
                required_type.append(type_dic[typ])
        list_type.append(required_type)

        
        for sk in skills_lower :
            if any(x in sk for x in ['+', '#', '.']):
                skk = re.escape(sk)
            else:
                skk = sk
            result = re.search(r'(?:^|(?<=\s))' + skk + r'(?=\s|$)',string)
            if result:
                required_skills.append(skills_dic[sk])
        list_skill.append(required_skills)

        
        for ed in edu_lower :
            if any(x in ed for x in ['+', '#', '.']):
                edd = re.escape(ed)
            else:
                edd = ed
            result = re.search(r'(?:^|(?<=\s))' + edd + r'(?=\s|$)', string)
            if result:
                required_edu.append(edu_dic[ed])
        list_edu.append(required_edu)

        
        for maj in major_lower :
            if any(x in maj for x in ['+', '#', '.']):
                majj = re.escape(maj)
            else:
                majj = maj
            result = re.search(r'(?:^|(?<=\s))' + majj + r'(?=\s|$)', string)
            if result:
                required_major.append(major_dic[maj])
        list_major.append(required_major)

        
        for key in keywords_lower :
            if any(x in key for x in ['+', '#', '.']):
                keyy = re.escape(key)
            else:
                keyy = key
            result = re.search(r'(?:^|(?<=\s))' + keyy + r'(?=\s|$)', string)
            if result:
                required_keywords.append(keywords_dic[key])
        list_keywords.append(required_keywords)

        
        words = string.split(' ')
        job_text = set(words) - set(stop_words) 
        list_text.append(list(job_text))
    except:
        list_type.append('Forbidden')
        list_skill.append('Forbidden')
        list_edu.append('Forbidden')
        list_major.append('Forbidden')
        list_keywords.append('Forbidden')
        list_text.append('Forbidden')
    print(i)

job_df_indeed['job_type'] = list_type
job_df_indeed['job_skills'] = list_skill
job_df_indeed['job_edu'] = list_edu
job_df_indeed['job_major'] = list_major
job_df_indeed['job_keywords'] = list_keywords
job_df_indeed['job_text'] = list_text

cols=['from','date','job_id','job_title','job_company','job_location','job_link','job_type',
        'job_skills', 'job_edu', 'job_major', 'job_keywords','job_text']
job_df_indeed = job_df_indeed[cols]


print(job_df_indeed.shape)
path = 'job_indeed_refine_' + now_str_name + '.csv'
job_df_indeed.to_csv(path)