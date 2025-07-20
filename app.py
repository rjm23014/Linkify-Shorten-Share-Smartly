from flask import Flask, render_template, request, redirect
from shortener import shorten_url
from qr_generator import generate_qr
from db import init_db, get_long_url, increment_visit, get_visits
import os

app = Flask(__name__)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = shorten_url(long_url)
        qr_code_path = generate_qr(short_url)
        short_code = short_url.split('/')[-1]
        visits = get_visits(short_code)
        return render_template('result.html', short_url=short_url, qr_image=qr_code_path, visits=visits)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_long(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        increment_visit(short_code)
        return redirect(long_url)
    return "<h1>URL not found</h1>", 404
