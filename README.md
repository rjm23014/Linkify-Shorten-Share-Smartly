# 🔗 Linkify - Modern URL Shortener

**Shorten your URLs with style!** A modern, fast, and secure URL shortener with QR code generation, user authentication, and analytics.

## ✨ Features

- 🚀 **Instant URL Shortening** - Lightning-fast link compression
- 📱 **QR Code Generation** - Automatic QR codes for every shortened URL  
- 🔐 **Google OAuth Login** - Secure authentication with Google accounts
- 📊 **Analytics Dashboard** - Track clicks and manage your links
- 💎 **Premium Features** - Purchase additional links (₹50 for 10 links)
- 🎨 **Modern UI** - Beautiful glassmorphism design
- 📱 **Mobile Responsive** - Works perfectly on all devices
- 🌙 **Dark Mode Support** - Automatic theme adaptation

## 🚀 Live Demo

Visit the live application: **[linkify-url-shortener.onrender.com](https://linkify-url-shortener.onrender.com)**

## �️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite  
- **Authentication**: Google OAuth 2.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern Glassmorphism UI
- **Deployment**: Render.com

## 🏃‍♂️ Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/rjm23014/Linkify-Shorten-Share-Smartly.git
   cd Linkify-Shorten-Share-Smartly
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Google OAuth credentials
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5001
   ```

## ⚙️ Environment Variables

Create a `.env` file with the following variables:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Flask Secret Key (generate a random string)
SECRET_KEY=your_secret_key_here

# Production Base URL (for deployment)
BASE_URL=https://your-domain.com
```

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized origins and redirect URIs:
   - **Local**: `http://localhost:5001`
   - **Production**: `https://your-domain.com`

## � Deployment on Render.com

This project is configured for easy deployment:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Deploy on Render**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository
   - Choose "Web Service"
   - Render will automatically detect the configuration

3. **Set Environment Variables**
   - Add your `GOOGLE_CLIENT_ID`
   - Add your `GOOGLE_CLIENT_SECRET`
   - `SECRET_KEY` will be auto-generated

4. **Update Google OAuth**
   - Add your Render domain to authorized origins
   - Format: `https://your-app-name.onrender.com`

## 💰 Pricing Model

- **Free Users**: 10 shortened URLs
- **Registered Users**: 10 free URLs + purchase options
- **Premium Package**: ₹50 for 10 additional URLs

## 👨‍💻 Author

**Made with ❤️ by Rajat Malik**

- GitHub: [@rjm23014](https://github.com/rjm23014)
- Project: [Linkify URL Shortener](https://github.com/rjm23014/Linkify-Shorten-Share-Smartly)

---

**⭐ Star this repository if you found it helpful!**
