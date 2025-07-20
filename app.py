from flask import Flask, render_template, request, redirect
from shortener import shorten_url
from qr_generator import generate_qr
from db import init_db, get_long_url, increment_visit, get_visits, save_to_db
import os
from flask import request
from time import time
rate_limit = {}
RATE_WINDOW = 60  # seconds

BASE_URL = "http://localhost:5000"


app = Flask(__name__)
init_db()
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()
        short_url = f"{BASE_URL}/{short_code}"

        save_to_db(long_url, short_code)

        qr_code_path = generate_qr(short_url)
        visits = get_visits(short_code)
        
        return render_template('result.html',
                               short_url=short_url,
                               qr_image=qr_code_path,
                               visits=visits)
    
    # GET request fallback (no short_code or short_url here!)
    return render_template('index.html')



@app.route('/<short_code>')
def redirect_to_long(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        increment_visit(short_code)
        return redirect(long_url)
    return "<h1>URL not found</h1>", 404


if __name__ == "__main__":
    init_db()  # initialize the database
    app.run(debug=True)
