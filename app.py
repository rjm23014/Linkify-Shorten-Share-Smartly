from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import requests
import json

from shortener import shorten_url
from qr_generator import generate_qr
from db import init_db, get_long_url, increment_visit, get_visits, save_to_db, create_user, get_user_by_google_id, get_user_urls, get_user_link_count, decrease_user_links, add_paid_links, get_user_by_id, update_user_urls_remaining
from user import User
from config import Config
import os
from time import time
import hashlib
rate_limit = {}
RATE_WINDOW = 60  # seconds
GUEST_USAGE_LIMIT = 3  # Maximum uses for guest users
GUEST_USAGE_WINDOW = 24 * 60 * 60  # 24 hours in seconds
FREE_LINKS_FOR_USERS = 10  # Free links for registered users
PAID_LINKS_PACKAGE = 10  # Links in paid package
PAID_PACKAGE_PRICE = 50  # INR 50 for 10 links

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
        return User(
            user_data[0],  # id
            user_data[1],  # google_id
            user_data[2],  # email
            user_data[3],  # name
            user_data[4],  # picture
            user_data[5] if len(user_data) > 5 else 10       # urls_remaining
        )
    return None

init_db()
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def get_client_identifier():
    """Get a unique identifier for the client (IP + User Agent)"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
    user_agent = request.environ.get('HTTP_USER_AGENT', '')
    return hashlib.md5(f"{client_ip}:{user_agent}".encode()).hexdigest()

def check_guest_usage_limit():
    """Check if guest user has exceeded usage limit"""
    if current_user.is_authenticated:
        return True  # Authenticated users have no limit
    
    client_id = get_client_identifier()
    current_time = time()
    
    # Clean old entries
    expired_time = current_time - GUEST_USAGE_WINDOW
    rate_limit[client_id] = [timestamp for timestamp in rate_limit.get(client_id, []) if timestamp > expired_time]
    
    # Check current usage
    usage_count = len(rate_limit.get(client_id, []))
    return usage_count < GUEST_USAGE_LIMIT

def record_guest_usage():
    """Record a usage for guest user"""
    if current_user.is_authenticated:
        return  # Don't track authenticated users
    
    client_id = get_client_identifier()
    current_time = time()
    
    if client_id not in rate_limit:
        rate_limit[client_id] = []
    
    rate_limit[client_id].append(current_time)

def get_remaining_guest_usage():
    """Get remaining usage count for guest user"""
    if current_user.is_authenticated:
        return float('inf')  # Unlimited for authenticated users
    
    client_id = get_client_identifier()
    current_time = time()
    
    # Clean old entries
    expired_time = current_time - GUEST_USAGE_WINDOW
    rate_limit[client_id] = [timestamp for timestamp in rate_limit.get(client_id, []) if timestamp > expired_time]
    
    usage_count = len(rate_limit.get(client_id, []))
    return max(0, GUEST_USAGE_LIMIT - usage_count)

@app.route('/', methods=['GET', 'POST'])
def index():
    remaining_usage = get_remaining_guest_usage()
    
    if request.method == 'POST':
        # Check limits based on user type
        if current_user.is_authenticated:
            if current_user.urls_remaining <= 0:
                flash(f'You have used all your available links! Purchase more links to continue.', 'error')
                return redirect(url_for('pricing'))
        else:
            # Guest user check
            if not check_guest_usage_limit():
                flash(f'Guest usage limit reached! You can only shorten {GUEST_USAGE_LIMIT} URLs per day. Please sign in for more access.', 'error')
                return render_template('index.html', remaining_usage=0, show_limit_reached=True)
        
        long_url = request.form['long_url']
        short_code = generate_short_code()
        short_url = f"{BASE_URL}/{short_code}"

        # Get user_id if logged in
        user_id = current_user.id if current_user.is_authenticated else None
        save_to_db(long_url, short_code, user_id)

        # Update usage tracking
        if current_user.is_authenticated:
            # Decrease user's remaining links
            new_remaining = current_user.urls_remaining - 1
            update_user_urls_remaining(current_user.id, new_remaining)
            current_user.urls_remaining = new_remaining
        else:
            # Record usage for guest users
            record_guest_usage()

        qr_code_path = generate_qr(short_url)
        visits = get_visits(short_code)
        
        return render_template('result.html',
                               short_url=short_url,
                               qr_image=qr_code_path,
                               visits=visits,
                               remaining_usage=get_remaining_guest_usage())
    
    # GET request
    user_remaining = current_user.urls_remaining if current_user.is_authenticated else None
    return render_template('index.html', 
                         remaining_usage=remaining_usage, 
                         user_remaining=user_remaining)



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
            user = User(
                user_data[0],  # id
                user_data[1],  # google_id
                user_data[2],  # email
                user_data[3],  # name
                user_data[4],  # picture
                user_data[5] if len(user_data) > 5 else 10       # urls_remaining
            )
        else:
            # Create new user
            user_id = create_user(google_id, email, name, picture)
            user = User(user_id, google_id, email, name, picture, 10)  # 10 free links for new users
        
        login_user(user)
        return {'success': True}
        
    except ValueError:
        return {'success': False, 'error': 'Invalid token'}, 400

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test-login')
def test_login():
    """Test login route for development - bypasses OAuth"""
    # Create or get test user
    test_google_id = "test_user_123"
    test_email = "test@example.com"
    test_name = "Test User"
    test_picture = "https://via.placeholder.com/50"
    
    # Check if test user exists
    user_data = get_user_by_google_id(test_google_id)
    if user_data:
        user = User(
            user_data[0],  # id
            user_data[1],  # google_id
            user_data[2],  # email
            user_data[3],  # name
            user_data[4],  # picture
            user_data[5] if len(user_data) > 5 else 10       # urls_remaining
        )
    else:
        # Create test user
        user_id = create_user(test_google_id, test_email, test_name, test_picture)
        user = User(user_id, test_google_id, test_email, test_name, test_picture, 10)
    
    login_user(user)
    return redirect(url_for('index'))

@app.route('/api/usage-status')
def usage_status():
    """API endpoint to get current usage status"""
    return jsonify({
        'remaining': get_remaining_guest_usage(),
        'limit': GUEST_USAGE_LIMIT,
        'is_authenticated': current_user.is_authenticated
    })

@app.route('/buy-links', methods=['POST'])
@login_required
def buy_links():
    """Simple payment endpoint - adds 10 links for ₹50"""
    try:
        # In a real app, this would integrate with a payment gateway
        # For now, we'll just add the links (assuming payment was successful)
        add_paid_links(current_user.id)
        
        # Update the current user's remaining links
        current_user.urls_remaining += 10
        
        return jsonify({
            'success': True,
            'message': 'Successfully purchased 10 additional links!',
            'new_remaining': current_user.urls_remaining
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Payment processing failed. Please try again.'
        }), 500

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing stats and purchase options"""
    user_urls = get_user_urls(current_user.id)
    return render_template('dashboard.html', 
                         user=current_user,
                         user_urls=user_urls,
                         urls_remaining=current_user.urls_remaining)


if __name__ == "__main__":
    init_db()  # initialize the database
    app.run(debug=True, port=5001)
