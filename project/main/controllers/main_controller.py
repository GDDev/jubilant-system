from flask import render_template, redirect, url_for, request
from flask_login import login_required

from project.main import main

@main.route('/', methods=['GET'])
@login_required
def home():
    if request.method == 'GET':
        return redirect(url_for('post.feed'))
    return render_template('terms.html')

@main.route('/termos', methods=['GET'])
def terms():
    return render_template('terms.html')
