# Mudra Patel
# ADB CSE 6331
# Assignment 2

from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,RadioField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import pandas as pd
import csv
import os
import pypyodbc

AZDBSERVER = 'mudra17.database.windows.net'
AZDBNAME = 'db1'
AZDBUSER = 'mudra'
AZDBPW = 'pwd'
AZDBDRIVER = '{ODBC Driver 17 for SQL Server}'

dsn = 'DRIVER='+AZDBDRIVER+';SERVER='+AZDBSERVER+';DATABASE='+AZDBNAME+';UID='+AZDBUSER+';PWD='+ AZDBPW
conn = pypyodbc.connect(dsn)
cursor = conn.cursor()
   

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configurations
app.config['SECRET_KEY'] = 'blah blah'

class SearchForm(FlaskForm):
    mag = StringField(
        'Magnitude:',
        [DataRequired()]
    )
    submit = SubmitField('Search earthquakes with greater magnitude')

class SearchForm2(FlaskForm):
    mag1 = StringField(
        'Magnitude 1:',
        [DataRequired()]
    )
    mag2 = StringField(
        'Magnitude 2:',
        [DataRequired()]
    )
    d=RadioField('Duration', choices=[('1','Last week'),('2','Last month')])
    submit = SubmitField('Search earthquakes with greater magnitude')

class SearchForm3(FlaskForm):
    lt = StringField(
        'Latitude:',
        [DataRequired()]
    )
    lg = StringField(
        'Longitude:',
        [DataRequired()]
    )
    submit = SubmitField('Search earthquakes with greater magnitude')


# Route to search based on magnitude 
@app.route('/',methods= ['GET', 'POST'])    
def mag():  
    form=SearchForm()
    x=form.mag.data
    if x:
        cursor.execute("SELECT * FROM dbo.all_month where mag>"+x)  
        data=cursor.fetchall() 
        cursor.execute("select * from INFORMATION_SCHEMA.columns where TABLE_NAME = N'all_month' ")
        cols_name=cursor.fetchall()
        return render_template('index.html',form=form,data=data,x=x,cols=cols_name)
    return render_template('index.html',form=form,data=None,x=None)

# Route to search based on magnitude range
@app.route('/magrange',methods= ['GET', 'POST'])    
def mag2():  
    form=SearchForm2()
    m1=form.mag1.data
    m2=form.mag2.data
    d=form.d.data
    if form.validate_on_submit():
        if d=="1":
            cursor.execute("select * from all_month where time > (select dateadd(week, -1, getdate())) and (mag between "+m1+" and "+ m2+")")
        elif d=="2":
            cursor.execute("select * from all_month where mag between "+m1+" and "+ m2)
        data=cursor.fetchall()
        cursor.execute("select * from INFORMATION_SCHEMA.columns where TABLE_NAME = N'all_month' ")
        cols_name=cursor.fetchall()
        return render_template('index.html',form=form,data=data,cols=cols_name)
    return render_template('index.html',form=form,data=None,cols=None)

# Route to search nearby earthquake based on given location 
@app.route('/nearby',methods= ['GET', 'POST'])    
def mag3():  
    form=SearchForm3()
    lg=form.lg.data
    lt=form.lt.data
    if form.validate_on_submit():
        cursor.execute("Declare @source geography = geography::Point("+lt+","+lg+",4326);select * from all_month where ((@source.STDistance(geography::Point(latitude, longitude, 4326))) / 1000)  < 300;")  
        data=cursor.fetchall() 
        cursor.execute("select * from INFORMATION_SCHEMA.columns where TABLE_NAME = N'all_month' ")
        cols_name=cursor.fetchall()
        return render_template('index.html',form=form,data=data,cols=cols_name)
    return render_template('index.html',form=form,data=None,x=None)


# Route to search earthquakes occuring at night based on magnitude 
@app.route('/night',methods= ['GET', 'POST'])    
def mag3():  
    form=SearchForm()
    mag=form.mag.data
    if form.validate_on_submit():
        cursor.execute("SELECT count(*) as 'number of earthquakes at night' FROM dbo.all_month where datepart(hour,time) in (1,2,3,4,5,20,21,22,23,24) and mag>"+mag)  
        data=cursor.fetchall() 
        cursor.execute("select * from INFORMATION_SCHEMA.columns where TABLE_NAME = N'all_month' ")
        cols_name=cursor.fetchall()
        return render_template('index.html',form=form,data=data,cols=cols_name)
    return render_template('index.html',form=form,data=None,x=None)
