---
## 🧠 AI Analysis Demo

![Resume Doctor AI Demonstration](https://github.com/TABISHCODING/resume-doctor.ai/blob/main/Untitled%20video%20-%20Made%20with%20Clipchamp%20(2).gif?raw=true)
WEBSITE LINK->https://resume-doctor-ai-frontend.onrender.com/us10_login.html
---
# 🩺 Resume Doctor AI - Complete Setup & Deployment Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Critical Fixes Applied](#critical-fixes-applied)
- [Deployment URLs](#deployment-urls)
- [Environment Variables](#environment-variables)
- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Resume Doctor AI is a comprehensive AI-powered resume analysis and job matching platform built with Flask (backend) and vanilla JavaScript (frontend). The application provides intelligent resume scanning, keyword extraction, job matching, and improvement suggestions.

### Key Features
- 🔐 User Authentication & Authorization
- 📄 Resume Upload & Analysis
- 💼 Job Description Management
- 🎯 AI-Powered Matching Algorithm
- 📊 Detailed Analytics & Scoring
- 💡 Intelligent Improvement Suggestions
- 📱 Responsive Web Interface

## 🏗️ Architecture

```
Resume-Doctor/
├── backend/                 # Flask API Server
│   ├── app_fixed.py        # Main application file
│   ├── models.py           # Database models
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic
│   └── requirements.txt    # Python dependencies
├── frontend/               # Static web interface
│   ├── *.html             # HTML pages
│   └── static/            # CSS, JS, assets
└── README.md              # This file
```

## 🔧 Critical Fixes Applied

### 1. **JWT Authentication Fix** ⚡
**Problem**: JWT tokens were failing verification immediately after login
**Root Cause**: Identity type mismatch (integer vs string)
**Solution**:
- Convert user ID to string when creating tokens: `identity=str(user.id)`
- Convert back to int for database queries: `int(get_jwt_identity())`
- Added helper functions in `models.py` for consistent handling

### 2. **Environment Variables Configuration** 🔑
**Problem**: JWT secrets not matching between generation and verification
**Solution**:
- Force JWT_SECRET_KEY to always match SECRET_KEY
- Enhanced environment variable loading with fallbacks
- Added comprehensive debugging logs

### 3. **Frontend Deployment Fixes** 🌐
**Problem**: Frontend redirects using incorrect paths for static deployment
**Solution**:
- Updated all redirects from `/dashboard` to `us10_dashboard.html`
- Fixed navigation links between pages
- Ensured proper static file serving

### 4. **Database Schema Optimization** 🗄️
**Improvements**:
- Added proper foreign key relationships
- Implemented cascade deletes for data integrity
- Added indexes for better query performance

## 🌍 Deployment URLs

### ✅ **Primary Application (Recommended)**
```
https://resume-doctor-ai.onrender.com
```
**Use this URL for:**
- Production use
- Sharing with friends/users
- Complete functionality (frontend + backend)

### 🔧 **Frontend-Only Deployment (Optional)**
```
https://resume-doctor-ai-frontend.onrender.com
```
**Note**: This is a separate static deployment for testing purposes

## 🔐 Environment Variables

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security Keys
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here  # Should match SECRET_KEY

# OpenAI API (for AI features)
OPENAI_API_KEY=your-openai-api-key-here

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

### ⚠️ **Important**: Environment Variables in Git
**DO NOT** commit `.env` files to Git repository for security reasons.
- Set environment variables directly in Render dashboard
- Use `.env.example` for documentation
- Keep sensitive keys secure

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/TABISHCODING/resume-doctor.ai.git
cd resume-doctor
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Setup Environment Variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. **Initialize Database**
```bash
python backend/init_db.py
```

6. **Run Application**
```bash
python backend/app_fixed.py
```

7. **Access Application**
- Open browser to `http://localhost:5000`

## 🌐 Production Deployment

### Render.com Deployment

1. **Connect GitHub Repository**
   - Link your GitHub repo to Render
   - Select `backend/app_fixed.py` as entry point

2. **Configure Environment Variables**
   - Add all required environment variables in Render dashboard
   - Ensure `JWT_SECRET_KEY` matches `SECRET_KEY`

3. **Database Setup**
   - Use Render PostgreSQL add-on
   - Set `DATABASE_URL` environment variable

4. **Deploy**
   - Render automatically deploys on git push
   - Monitor logs for any issues

### Frontend Deployment (Optional)
- Deploy `frontend/` directory as static site
- Ensure `config.js` points to correct backend URL

## 🗄️ Database Management

### Fresh Start (Clear All Data)
```python
# Run this script to clear all data while keeping schema
python backend/clear_data.py
```

### Manual Database Reset
```sql
-- Connect to your database and run:
TRUNCATE TABLE scan_history, job_descriptions, resumes, users RESTART IDENTITY CASCADE;
```

### Backup Database
```bash
pg_dump $DATABASE_URL > backup.sql
```

## 🔍 Troubleshooting

### Common Issues

#### 1. **Authentication Fails**
- Check JWT secrets match in environment variables
- Verify token format in browser localStorage
- Check server logs for JWT errors

#### 2. **Frontend Not Loading**
- Verify API_BASE_URL in `frontend/static/js/config.js`
- Check CORS configuration in backend
- Ensure all redirects use correct file paths

#### 3. **Database Connection Issues**
- Verify DATABASE_URL format
- Check PostgreSQL service status
- Ensure database exists and is accessible

#### 4. **502 Bad Gateway**
- Wait for deployment to complete (90+ seconds)
- Check Render service logs
- Verify all environment variables are set

### Debug Commands
```bash
# Test authentication flow
python backend/test_auth_flow.py

# Test JWT generation
python backend/test_jwt_generation.py

# Check API endpoints
python backend/simple_test.py
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review server logs in Render dashboard
3. Test with provided debug scripts
4. Verify environment variable configuration

## 🎉 Success Indicators

✅ **Application is working correctly when:**
- Login redirects to dashboard successfully
- Dashboard loads user data
- Resume upload and analysis works
- Job matching provides results
- All navigation links work properly

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
