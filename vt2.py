from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SelectField, widgets, SelectMultipleField, ValidationError

class Arvosanalaskuri(FlaskForm):
    etunimi     = StringField('Etunimi')
    sukunimi    = StringField('Sukunimi')


app = Flask(__name__)
@app.route('/wtlomake', methods=['POST','GET']) 
def wtlomake():
    form = Arvosanalaskuri(csrf_enabled=False)
    return render_template('wtlomake.html', form=form)