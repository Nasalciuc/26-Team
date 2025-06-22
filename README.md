# Market Spark - AI-Powered Marketing Platform

## 🇷🇴 Descrierea Proiectului (Romanian)

**Market Spark** este o platformă avansată de marketing digital care oferă servicii complete de marketing bazate pe analiza site-ului web al utilizatorului. Aplicația oferă funcționalități complete pentru:

- **Analiza site-ului**: Scraping automat al site-ului web al utilizatorului pentru a înțelege conținutul și structura
- **Generarea de persoane**: Crearea de buyer personas personalizate folosind AI bazat pe analiza site-ului
- **Strategii de marketing**: Dezvoltarea de strategii personalizate bazate pe conținutul site-ului
- **Generarea de conținut**: Crearea automată de postări și imagini cu AI inspirate din site-ul utilizatorului
- **Postare automată**: Integrare cu Facebook pentru postarea automată a conținutului generat

Platforma analizează site-ul web al utilizatorului și generează automat întregul plan de marketing - de la persoanele țintă până la conținutul pentru social media. Este construită cu Django și PostgreSQL, rulează în containere Docker și integrează API-uri moderne pentru generarea de conținut și analiza datelor.

---

## 🇺🇸 Project Description (English)

**Market Spark** is an advanced digital marketing platform that provides comprehensive marketing services based on analysis of the user's website. The application offers complete functionality for:

- **Website Analysis**: Automated scraping of the user's website to understand content and structure
- **Persona Generation**: AI-powered creation of customized buyer personas based on website analysis
- **Marketing Strategies**: Development of personalized strategies based on website content
- **Content Generation**: Automated creation of posts and images using AI inspired by the user's website
- **Auto Posting**: Facebook integration for automatic posting of generated content

The platform analyzes the user's website and automatically generates the entire marketing plan - from target personas to social media content. It is built with Django and PostgreSQL, runs in Docker containers, and integrates modern APIs for content generation and data analysis.

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git
- At least 4GB RAM available

### 1. Clone the Repository
```bash
git clone git@github.com:Nicu106/26-Team.git
cd team26
```

### 2. Environment Setup
```bash
# Automatic setup (recommended)
./setup-env.sh

# OR manual setup
cp env.example .env
```

### 3. Start the Application
```bash
# Build and start all containers
docker-compose up --build
```

**That's it!** 🎉

The startup script will automatically:
- ✅ Wait for the database to be ready
- ✅ Run all migrations
- ✅ Create a superuser from environment variables
- ✅ Start the Django server

## 🌐 Access the Application

- **Main Application**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
  - **Username**: admin (configurable in .env)
  - **Password**: admin123 (configurable in .env)

## 🔧 Environment Configuration

### Available Variables in `.env`:

```env
# PostgreSQL Database Configuration
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Connection
DB_ENGINE=django.db.backends.postgresql
DB_HOST=db
DB_PORT=5432

# Admin User Configuration
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# Application Settings
APP_NAME=Team26 Django App
APP_VERSION=1.0.0
TIME_ZONE=UTC
LANGUAGE_CODE=en-us

# Development Settings
DEVELOPMENT_MODE=True
LOG_LEVEL=DEBUG

# Facebook Integration (for auto-posting)
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# OpenAI Integration (for AI content generation)
OPENAI_API_KEY=your_openai_api_key
```

### Customization:

1. **Change admin password**:
   ```env
   ADMIN_PASSWORD=your_secure_password
   ```

2. **Change database name**:
   ```env
   POSTGRES_DB=your_database_name
   ```

3. **Disable debug mode**:
   ```env
   DJANGO_DEBUG=False
   ```

## 🛠️ Useful Commands

### Run in background
```bash
docker-compose up -d --build
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

### Check logs
```bash
docker-compose logs web
docker-compose logs db
```

### Access Django shell
```bash
docker-compose run web python manage.py shell
```

### Create superuser manually
```bash
docker-compose run web python manage.py createsuperuser
```

### Regenerate .env file
```bash
./setup-env.sh
```

## 📊 Database

- **Type**: PostgreSQL 15
- **Host**: localhost:5432
- **Database**: django_db (configurable)
- **User**: django_user (configurable)
- **Password**: django_pass (configurable)

## 📁 Project Structure

```
team26/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── env.example
├── setup-env.sh
├── startup.sh
├── manage.py
├── README.md
├── auth_app/              ← Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── facebook_poster.py
│   ├── image_generator.py
│   └── templates/
├── web/                   ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                 ← Generated images
├── templates/             ← HTML templates
└── staticfiles/           ← Static files
```

## 📝 Important Notes

1. Ensure Docker and Docker Compose are installed and running
2. Port 8000 must be free for the Django application
3. Port 5432 must be free for PostgreSQL
4. First run may take longer due to Docker image downloads
5. Superuser is automatically created on first run from environment variables
6. All settings are configurable through the `.env` file
7. For Facebook auto-posting, you need a valid Facebook access token
8. For AI content generation, you need a valid OpenAI API key
9. The platform analyzes your own website to generate marketing content
10. All marketing strategies are personalized based on your website content

## 🐛 Troubleshooting

### If Docker doesn't start
```bash
# Check Docker status
docker --version
docker-compose --version

# Restart Docker Desktop
```

### If ports are occupied
```bash
# Check what's running on ports
lsof -i :8000
lsof -i :5432

# Modify ports in docker-compose.yml if necessary
```

### If migrations fail
```bash
# Remove volumes and start fresh
docker-compose down -v
docker-compose up --build
```

### If you want to reset everything
```bash
# Stop and remove everything
docker-compose down -v
```

### If Facebook posting doesn't work
```bash
# Check if ngrok is running for public URL access
ngrok http 8000

# Update ALLOWED_HOSTS in web/settings.py with ngrok URL
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 