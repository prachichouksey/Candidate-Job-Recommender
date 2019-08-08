# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 16:21:34 2019

@author: prach
"""
import nltk, re
from word2number import w2n
import pandas as pd

class ExtractExp:
    
    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []
    max_weightage = 40;
    min_variance = 5
    
    def get_features(self, text): 
        
       
        self.preprocess_data(text)
        self.tokenize(text)
        return self.get_exp(text)
            
    def preprocess_data(self, document):
        
        try:
            try:
                document = document.decode('ascii', 'ignore')
            except:
                pass
            
            lines = [el.strip() for el in re.split("\r|\n",document) if len(el) > 0]  
            lines = [nltk.word_tokenize(el) for el in lines]    
            lines = [nltk.pos_tag(el) for el in lines]  
            
            sentences = nltk.sent_tokenize(document)    
            sentences = [nltk.word_tokenize(sent) for sent in sentences]    
            tokens = sentences
            sentences = [nltk.pos_tag(sent) for sent in sentences]    
            dummy = []
            for el in tokens:
                dummy += el
            tokens = dummy
            
            return tokens, lines, sentences
        except Exception as e:
            print(e)
    
    def tokenize(self, inputString):
        try:
            self.tokens, self.lines, self.sentences = self.preprocess_data(inputString)
            return self.tokens, self.lines, self.sentences
        except Exception as e:
            print(e)
    
    def get_exp(self,inputString):
        expMatchStrings = ['experience', 'exp ', 'exp.', 'exp:','experience:']
        
        yearStrings = ['yrs', 'years', 'yr']
        experience = []
        experience_df=pd.DataFrame(columns=('Type', 'Years', 'Months', 'Location'))
        try:
            pos = 0
            for sentence in self.lines:
                pos = pos+1
                sen=" ".join([words[0].lower() for words in sentence]) 
                if any(re.search(x,sen) for x in expMatchStrings) and any(re.search(x,sen) for x in yearStrings):
                    sen_tokenised= nltk.word_tokenize(sen)
                    tagged = nltk.pos_tag(sen_tokenised)
                    entities = nltk.chunk.ne_chunk(tagged)
                    for subtree in entities.subtrees():
                        for leaf in subtree.leaves():
                            if leaf[1]=='CD':
                                if re.search('total',sen):
                                    expType = 1
                                else: 
                                    if re.search('overall',sen):
                                        expType = 2
                                    else:
                                        expType = 3
                                        
                                expStr = leaf[0].strip('+').strip('\x07')
                                
                                for match in (expMatchStrings+yearStrings):
                                    expStr = expStr.replace(match,"")
                                    try:
                                        years = float(expStr)
                                    except:
                                        try:
                                           
                                            years = w2n.word_to_num(expStr)
                                        except:
                                           
                                            non_decimal = re.compile(r'[^\d.]+')
                                            expStr=non_decimal.sub("", expStr)
                                            try:
                                                years = float(expStr)
                                            except Exception as e:
                                                years = 0
                                                print(e)
                            
                                    if years>0 and years < 30:
                                        experience_df = experience_df.append({'Type': expType, 'Years': years, 'Months': 0, 'Location': pos},ignore_index=True)                                    
                                                                                
            if not experience_df.empty:
                
                experience_df = experience_df.sort_values(['Type', 'Years'], ascending=[True, False])
                experience = float(experience_df['Years'].iloc[0])
            else:
                experience = 0.0
                        
        except Exception as e:
            print (e)
            
        return experience

    def get_exp_weightage(self,jd_exp,resume_exp):
        
        score = 0
        print(resume_exp)
        resume_exp = int(round(resume_exp))
        if jd_exp.find("-") == -1:
            jd_exp = "0-"+jd_exp[:]
            
        min_jd_exp =  int(jd_exp[0])
        max_jd_exp = int(jd_exp[2])
        
        if resume_exp == 0:
            score = 0
            
        elif resume_exp > min_jd_exp:
            if resume_exp > max_jd_exp:
                score = self.max_weightage - (self.min_variance*(resume_exp-max_jd_exp))
            else:
                score = self.max_weightage
                
        else:
            score = self.max_weightage - (self.min_variance*(min_jd_exp-resume_exp))
        
        if score < 0:
            score = 0
        return score 