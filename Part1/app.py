from ast import keyword
from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import pandas as pd
from PIL import Image
import base64
import io
import csv
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configurations
app.config['SECRET_KEY'] = 'blah blah'

class SearchForm(FlaskForm):
    name = StringField(
        'Name:',
        [DataRequired()]
    )
    submit = SubmitField('Display image')

class DeleteForm(FlaskForm):
    name = StringField(
        'Name:',
        [DataRequired()]
    )
    submit = SubmitField('Delete person')

class Salary(FlaskForm):
    salary=StringField('Salary:')
    submit = SubmitField('Search for people with salary less than above')

class Keyword(FlaskForm):
    name=StringField(
        'Name:',
        [DataRequired()]
    )
    keyword=StringField('Keyword:')
    submit = SubmitField('Change keyword')

class AddForm(FlaskForm):
    name=StringField(
        'Name:',
        [DataRequired()]
    )
    photo = FileField('Photo',validators=[FileRequired()])
    submit = SubmitField('Add Photo')


@app.route('/delete',methods=['GET','POST'])
def delete():
    form = DeleteForm()
    name = form.name.data
    with open('static\\people.csv', 'r') as read_obj:
        dict_reader = csv.DictReader(read_obj)
        list_of_dict = list(dict_reader)
    if form.validate_on_submit():
        for i in range(len(list_of_dict)):
            if list_of_dict[i]["Name"]==name:
                del list_of_dict[i]
                message="Successful deletion"
                break
        keys = list_of_dict[0].keys()

        with open('static\\people.csv', 'w', newline='') as output_file:
          dict_writer = csv.DictWriter(output_file, keys)
          dict_writer.writeheader()
          dict_writer.writerows(list_of_dict)
        return render_template('del.html',form=form,mes=message,name=name)
    return render_template('del.html',form=form,mes=None,name=None)

@app.route('/addphoto',methods=['GET','POST'])
def add():
    form=AddForm()
    name=form.name.data
    f = form.photo.data
    with open('static\\people.csv', 'r') as read_obj:
        dict_reader = csv.DictReader(read_obj)
        list_of_dict = list(dict_reader)
    if form.validate_on_submit():
        for i in list_of_dict:
          if i["Name"]==name:
            if len(i["Picture"])>3:
                message="Photo already exists"
                break
            else:
                message="Photo added successfully"
                filename = secure_filename(f.filename)
                f.save(os.path.join('static\\', filename))
                i["Picture"]=filename
                keys = list_of_dict[0].keys()
                with open('static\\people.csv', 'w', newline='') as output_file:
                 dict_writer = csv.DictWriter(output_file, keys)
                 dict_writer.writeheader()
                 dict_writer.writerows(list_of_dict)
                break
        return render_template('add.html',form=form,file=f,mes=message)
    return render_template('add.html',form=form,file=None,mes=None)

@app.route('/changekeyword',methods=['GET','POST'])
def changeKeyW():
    form = Keyword()
    name = form.name.data
    keyw=form.keyword.data
    with open('static\\people.csv', 'r') as read_obj:
        dict_reader = csv.DictReader(read_obj)
        list_of_dict = list(dict_reader)

    if form.validate_on_submit():
        for i in list_of_dict:
         if i["Name"]==name:
             i["Keywords"]=keyw
             message="Keywords changed successfully"
             break

        keys = list_of_dict[0].keys()
        with open('static\\people.csv', 'w', newline='') as output_file:
         dict_writer = csv.DictWriter(output_file, keys)
         dict_writer.writeheader()
         dict_writer.writerows(list_of_dict)
        return render_template('changekey.html',form=form,keyw=keyw,mes=message)
    return render_template('changekey.html',form=form,mes=None)

@app.route('/',methods=['GET','POST'])
def index():
    form = SearchForm()
    name = form.name.data
    with open('static\\people.csv', 'r') as read_obj:
        dict_reader = csv.DictReader(read_obj)
        list_of_dict = list(dict_reader)
    if form.validate_on_submit():
        for i in list_of_dict:
         if i["Name"]==name:
            path=i["Picture"]
            path1="static\\"+path
            im=Image.open(path1)
            data = io.BytesIO()
            im.save(data, "JPEG")
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template('index.html',form=form,name=name,img_data=encoded_img_data.decode('utf-8'))
    return render_template('index.html',form=form,name=name)

   
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)
