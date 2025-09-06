# Trackify - Personal Finance Tracker

Trackify is a comprehensive personal finance management application built with Django that helps users track their expenses, income, and financial goals with ease and precision.

## Features

### 💰 Expense Tracking
- Upload receipts and automatically extract expense details using AI
- Manual expense entry with category classification
- Currency conversion support
- Expense categorization and analysis

### 💵 Income Management
- Track multiple income sources
- Income categorization
- Historical income tracking

### 📊 Dashboard & Analytics
- Interactive dashboard with expense visualization
- Category-wise spending analysis
- Financial balance tracking
- Monthly/yearly summaries

### 🔐 User Management
- Secure user authentication
- Profile management
- Password reset functionality

## Technology Stack

- **Backend**: Django 5.1.2
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Integration**: OpenAI GPT-4 for receipt processing
- **Charts**: Chart.js for data visualization
- **Authentication**: Django's built-in auth system

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trackify
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin/

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
OPEN_EXCHANGE_RATES_API_KEY=your-exchange-rates-api-key
DATABASE_URL=sqlite:///db.sqlite3
```

### API Keys Required

- **OpenAI API Key**: For receipt processing and expense extraction
- **Open Exchange Rates API Key**: For currency conversion

## Project Structure

```
trackify/
├── budgetlens/           # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Main application
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── static/
├── accounts/             # User management
├── docs/                 # Documentation
├── media/                # User uploaded files
└── static/               # Static files
```

## Usage

### Adding Expenses

1. **Manual Entry**: Use the "Add Expense" form
2. **Receipt Upload**: Upload receipt images for automatic processing
3. **Categories**: Choose from predefined categories or create custom ones

### Managing Income

1. Navigate to Income section
2. Add income entries with sources and amounts
3. Track income history and patterns

### Dashboard

- View expense summaries by category
- Monitor spending trends
- Track financial balance
- Generate reports

## API Documentation

The application provides RESTful APIs for:
- Expense management
- Income tracking
- User profile management
- Currency conversion

See [API Documentation](./api.md) for detailed endpoints.

## Deployment

### Development
```bash
python manage.py runserver
```

### Production
See [Deployment Guide](./deployment.md) for production deployment instructions.

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Support

For support, email support@trackify.com or join our Slack community.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.
