from flask import Flask, request, render_template
from wtforms import Form, StringField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length

import smtplib
from email.message import EmailMessage

import os
smtp_host = os.environ['SMTP_HOST']
smtp_user = os.environ['SMTP_USER']
smtp_pass = os.environ['SMTP_PASS']
shoutbomb_email = os.environ['SHOUTBOMB_EMAIL']

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

def send_reg(form):
    lang_codes = {'en': 'WEBSIGNUP', 'es': 'WEBREGISTRESE'}
    lang = lang_codes[form.lang.data]
    phone = form.phone.data
    barcode = form.barcode.data
    subject = '({}+TWILIO+{}+{});'.format(lang, phone, barcode)

    msg = EmailMessage()
    msg['From'] = smtp_user
    msg['To'] = shoutbomb_email
    msg['Subject'] = subject

    s = smtplib.SMTP_SSL(smtp_host)
    s.login(smtp_user, smtp_pass)
    s.send_message(msg)
    s.quit()

class RegForm(Form):
    lang = RadioField('Language', choices=[('en','English'), ('es','Español')])
    phone = StringField('Mobile Phone Number',
                        [DataRequired(), Length(min=10, max=10)])
    barcode = StringField('Library Card Number',
                          [DataRequired(), Length(min=14, max=14)])
    accept_tos = BooleanField('I accept the terms of service',
                              [DataRequired()])

@app.route('/shoutbomb', methods=['GET', 'POST'])
def login():
    form = RegForm(request.form)
    if not request.form:
        form.lang.default = 'en'
        form.process()
    if request.method == 'POST' and form.validate():
        send_reg(form)
        return render_template('success.html', form=form)
    return render_template('register.html', form=form)
