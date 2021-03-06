from flask import Flask, request, render_template
from wtforms import Form, StringField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length

import smtplib

import os
smtp_host = os.environ['SMTP_HOST']
smtp_user = os.environ['SMTP_USER']
shoutbomb_email = os.environ['SHOUTBOMB_EMAIL']

app = Flask(__name__)

def send_reg(form):
    lang_codes = {'en': 'WEBSIGNUP', 'es': 'WEBREGISTRESE'}
    lang = lang_codes[form.lang.data]
    phone = form.phone.data
    barcode = form.barcode.data
    subject = '({}+TWILIO+{}+{});'.format(lang, phone, barcode)
    message = 'Subject: {}\n\n'.format(subject)
    s = smtplib.SMTP(smtp_host)
    s.sendmail(smtp_user, shoutbomb_email, message)
    s.quit()

class RegForm(Form):
    lang = RadioField('Language', choices=[('en','English'), ('es','Español')])
    phone = StringField('Mobile Phone Number',
                        [DataRequired(), Length(min=10, max=10, message='Please enter your 10-digit mobile phone number as 1234567890 without parentheses, dashes, and spaces.')])
    barcode = StringField('Library Card Number',
                          [DataRequired(), Length(min=14, max=14, message='Please enter your 14-digit library card number, without spaces.')])
    accept_tos = BooleanField('Click here to acknowledge', [DataRequired()])

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
