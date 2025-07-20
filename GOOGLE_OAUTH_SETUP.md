# Google OAuth Setup Guide

## Setting up Google OAuth for Linkify

To enable Google Sign-In for your Linkify app, follow these steps:

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google Identity API)

### 2. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client IDs**
3. Configure the OAuth consent screen if prompted
4. Choose **Web application** as the application type
5. Add authorized redirect URIs:
   - `http://localhost:5000/auth/google` (for local development)
   - Add your production domain when deploying

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Google OAuth credentials:
   ```
   GOOGLE_CLIENT_ID=your_actual_google_client_id
   GOOGLE_CLIENT_SECRET=your_actual_google_client_secret
   SECRET_KEY=your_random_secret_key_here
   ```

3. Generate a secret key:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

### 4. Update your config.py

Make sure your `config.py` loads from environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
```

### 5. Install python-dotenv

```bash
pip install python-dotenv
```

### 6. Run the Application

```bash
python app.py
```

## Features Added

- **Google Sign-In**: Users can sign in with their Google account
- **User Dashboard**: Authenticated users can view their shortened URLs
- **URL Tracking**: URLs are associated with user accounts
- **Navigation Bar**: Clean navigation with user profile info
- **Guest Mode**: Users can still use the app without signing in

## File Structure

```
├── app.py              # Main Flask application with OAuth
├── config.py           # Configuration settings
├── user.py             # User model for Flask-Login
├── db.py               # Database functions (updated with user support)
├── templates/
│   ├── navbar.html     # Navigation bar component
│   ├── login.html      # Google Sign-In page
│   ├── dashboard.html  # User dashboard
│   ├── index.html      # Updated home page
│   └── result.html     # Updated result page
├── static/
│   └── style.css       # Updated styles with navbar and dashboard
└── requirements.txt    # Updated dependencies
```

## Next Steps

1. Set up your Google OAuth credentials
2. Configure your environment variables
3. Test the sign-in functionality
4. Deploy to production with HTTPS for security
