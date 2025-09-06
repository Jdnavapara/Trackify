# Installation Guide

This guide will help you set up Trackify on your local development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **Virtual environment support** (venv)

### Checking Prerequisites

```bash
# Check Python version
python --version
# Should show Python 3.8 or higher

# Check pip
pip --version

# Check git
git --version
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd trackify
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your command prompt after activation.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Django settings
DEBUG=True
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=sqlite:///db.sqlite3


# Email (optional, for password reset)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Static Files (Development)

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/

## API Keys Setup

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Add it to your `.env` file

### Open Exchange Rates API Key

1. Go to [Open Exchange Rates](https://openexchangerates.org/)
2. Sign up for a free account
3. Get your API key
4. Add it to your `.env` file

## Troubleshooting

### Common Issues

#### 1. Virtual Environment Issues

```bash
# If activation doesn't work on Windows
python -m venv .venv
.venv\Scripts\activate.bat

# If pip install fails
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Database Issues

```bash
# Reset database
python manage.py flush
python manage.py migrate
```

#### 3. Static Files Issues

```bash
# Clear static files cache
python manage.py collectstatic --clear --noinput
```

#### 4. Permission Issues

```bash
# On Linux/Mac, make scripts executable
chmod +x manage.py
```

### Environment Variables Not Loading

Ensure your `.env` file is in the project root and contains the correct values. You can verify by checking Django settings:

```python
python manage.py shell
from django.conf import settings
print(settings.DEBUG)
print(settings.SECRET_KEY)
```

## Next Steps

After successful installation:

1. **Create a regular user account** through the signup page
2. **Upload some receipts** to test the AI functionality
3. **Add manual expenses** to test the expense tracking
4. **Explore the dashboard** to see your financial overview

## Production Deployment

For production deployment, see the [Deployment Guide](./deployment.md).

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [README.md](./README.md) for additional information
3. Check existing GitHub issues
4. Create a new issue with detailed error messages
