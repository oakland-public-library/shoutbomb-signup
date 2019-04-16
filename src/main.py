from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    phone = StringField('Mobile Phone Number', [DataRequired(), Length(min=4, max=25)])
    card = StringField('Library Card Number', [DataRequired(), Length(min=6, max=35)])
    accept_tos = BooleanField('I accept the terms of service', [DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('ok')
    else:
        print('ok')
    form = MyForm()
    return render_template('register.html', form=form)
