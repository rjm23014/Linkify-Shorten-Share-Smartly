from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import requests
import json

from shortener import shorten_url
from qr_generator import generate_qr
from db import init_db, get_long_url, increment_visit, get_visits, save_to_db, create_user, get_user_by_google_id, get_user_urls
from user import User
from config import Config
import os
from time import time
rate_limit = {}
RATE_WINDOW = 60  # seconds

BASE_URL = "http://localhost:5001"

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # This would typically load from database
    from db import get_user_by_id
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
    return None

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

        # Get user_id if logged in
        user_id = current_user.id if current_user.is_authenticated else None
        save_to_db(long_url, short_code, user_id)

        qr_code_path = generate_qr(short_url)
        visits = get_visits(short_code)
        
        return render_template('result.html',
                               short_url=short_url,
                               qr_image=qr_code_path,
                               visits=visits)
    
    # GET request
    return render_template('index.html')



@app.route('/<short_code>')
def redirect_to_long(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        increment_visit(short_code)
        return redirect(long_url)
    return "<h1>URL not found</h1>", 404

@app.route('/login')
def login():
    return render_template('login.html', google_client_id=app.config['GOOGLE_CLIENT_ID'])

@app.route('/auth/google', methods=['POST'])
def google_auth():
    token = request.json.get('token')
    
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), app.config['GOOGLE_CLIENT_ID'])
        
        # Get user info
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo.get('picture', '')
        
        # Check if user exists
        user_data = get_user_by_google_id(google_id)
        
        if user_data:
            # User exists, log them in
            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        else:
            # Create new user
            user_id = create_user(google_id, email, name, picture)
            user = User(user_id, google_id, email, name, picture)
        
        login_user(user)
        return {'success': True}
        
    except ValueError:
        return {'success': False, 'error': 'Invalid token'}, 400

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_urls = get_user_urls(current_user.id)
    return render_template('dashboard.html', urls=user_urls)


if __name__ == "__main__":
    init_db()  # initialize the database
    app.run(debug=True, port=5001)
