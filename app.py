from flask import Flask, render_template, request, redirect, url_for
from shortener import shorten_url
from qr_generator import generate_qr
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = shorten_url(long_url)
        qr_code_path = generate_qr(short_url)
        return render_template('result.html', short_url=short_url, qr_image=qr_code_path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
