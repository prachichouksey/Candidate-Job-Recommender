# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 16:21:34 2019

@author: prach
"""
import glob
import os
import warnings
from flask import (Flask,session,flash, redirect, render_template, request,
                   url_for, send_from_directory)
import core
import search
import pandas as pd


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) 
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin',
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Upload-Resume'
app.config['UPLOAD_JD_FOLDER'] = 'Upload-JD'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'doc', 'docx'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
     
    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        os.chdir(app.config['UPLOAD_JD_FOLDER'])
        file = glob.glob('*.xlsx', recursive=False)
        data_set = pd.read_excel(file[0])
        search_st = data_set['High Level Job Description'][0]
        skill_text = data_set['Technology'][0] + data_set['Primary Skill'][0]
        jd_exp = data_set['Yrs Of Exp '][0]
        title = data_set['Job Title'][0]
        flask_return = core.res(search_st,skill_text,jd_exp)
        df = pd.DataFrame(columns=['Title','Experience','Primary Skill','Technology'])
        df = df.append({'Title': title,'Experience':jd_exp,'Primary Skill':data_set['Primary Skill'][0],'Technology':data_set['Technology'][0]}, ignore_index=True)
        return render_template('result.html', results = flask_return,jd = df)

@app.route('/uploadResume', methods=['GET', 'POST'])
def uploadResume():
    return render_template('uploadresume.html')

@app.route("/upload", methods=['POST'])
def upload_file():
   
    print("resume-resume",os.getcwd())
    if request.method=='POST' and 'customerfile' in request.files:
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            
        x = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template("resultlist.html", name=x)
    
@app.route('/uploadjdDesc', methods=['GET', 'POST'])
def uploadjdDesc():
    return render_template('uploadjd.html')

@app.route("/uploadjd", methods=['POST'])
def upload_jd_file():
    
    print("resume-jd",os.getcwd())
    if request.method=='POST' and 'customerfile' in request.files:
        filelist = [ f for f in os.listdir(app.config['UPLOAD_JD_FOLDER']) if f.endswith(".xlsx") ]
        for f in filelist:
             os.remove(os.path.join(app.config['UPLOAD_JD_FOLDER'], f))
        
        for f in request.files.getlist('customerfile'):
            f.save(os.path.join(app.config['UPLOAD_JD_FOLDER'], f.filename))
            
        x = os.listdir(app.config['UPLOAD_JD_FOLDER'])
        return render_template("resultlist.html", name=x)
		

@app.route('/resultsearch' ,methods = ['POST', 'GET'])
def resultsearch():
    os.chdir(app.config['UPLOAD_JD_FOLDER'])
    file = glob.glob('*.xlsx', recursive=False)
    data_set = pd.read_excel(file[0])
    search_st = data_set['High Level Job Description'][0]
    result = search.res(search_st)
    return render_template('result.html', results = result)

@app.route('/Upload-Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Upload-Resume', filename)



if __name__ == '__main__':
    app.run('0.0.0.0' , 3000 , debug=True , threaded=True)
    
