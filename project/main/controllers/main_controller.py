import requests
from flask import render_template
from flask_login import login_required

from project.main import main

@main.route('/', methods=['GET',])
@login_required
def home():
    return render_template('index.html')

@main.route('/termos')
def terms():
    return render_template('terms.html')
