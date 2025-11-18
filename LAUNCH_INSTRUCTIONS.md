# 🚀 Application Launch Instructions

This document provides comprehensive instructions for launching and using the integrated Tinkerbell application.

## 📋 Prerequisites

Before launching the application, ensure you have:

- ✅ Docker and Docker Compose installed and running
- ✅ Node.js (v14 or higher) installed
- ✅ At least 4GB of available RAM
- ✅ Ports 8000 and 8081 available

## 🎯 Quick Start (Automated)

The easiest way to launch the application is using the automated launch script:

```bash
./launch_application.sh
```

This script will:
1. Create the `.env` file if it doesn't exist
2. Start Docker containers (Django backend + PostgreSQL database)
3. Run database migrations
4. Create a superuser
5. Start the Tinkerbell frontend server
6. Verify both services are running

## 🛑 Stopping the Application

To stop all services:

```bash
./stop_application.sh
```

Or manually:

```bash
# Stop Docker containers
docker compose down

# Stop frontend server
kill $(lsof -t -i:8081)
```

## 🔧 Manual Launch (Step by Step)

If you prefer to launch components manually:

### 1. Setup Environment

```bash
# Create .env file from template
cp env.example .env
```

### 2. Start Backend Services

```bash
# Start Docker containers (Django + PostgreSQL)
docker compose up -d --build

# Wait for services to be ready (about 10-15 seconds)
# Check logs
docker compose logs -f web
```

### 3. Start Frontend Server

```bash
# Navigate to frontend directory
cd tinkerbell-frontend

# Start the Node.js server
node server.js
```

Or run in background:

```bash
cd tinkerbell-frontend
nohup node server.js > /tmp/tinkerbell-frontend.log 2>&1 &
```

## 🌐 Accessing the Application

Once launched, you can access:

### Frontend (Tinkerbell)
- **URL**: http://localhost:8081
- **Landing Page**: http://localhost:8081/
- **App Interface**: http://localhost:8081/app
- **Dashboard**: http://localhost:8081/dashboard

### Backend (Django)
- **URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Login Page**: http://localhost:8000/auth_app/login/
- **API Endpoints**: http://localhost:8000/auth_app/api/...

### Admin Credentials

Default superuser credentials (configurable in `.env`):
- **Username**: `admin`
- **Password**: `admin123`

## 📊 Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                             │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                    │
        ▼                                    ▼
┌──────────────────┐              ┌──────────────────┐
│   Tinkerbell     │              │  Django Backend  │
│   Frontend       │◄────────────►│   (REST API)     │
│   (Port 8081)    │   CORS       │   (Port 8000)    │
│   Node.js Server │              │   Docker         │
└──────────────────┘              └──────────────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │   PostgreSQL     │
                                  │   Database       │
                                  │   (Port 5432)    │
                                  │   Docker         │
                                  └──────────────────┘
```

## 🔍 Verification & Testing

### Check Services Status

```bash
# Check if ports are listening
netstat -tlnp | grep -E ":(8000|8081|5432)"

# Or using ss
ss -tlnp | grep -E ":(8000|8081|5432)"
```

### Test Backend

```bash
# Health check
curl http://localhost:8000/

# Check admin panel
curl http://localhost:8000/admin/
```

### Test Frontend

```bash
# Landing page
curl http://localhost:8081/

# App interface
curl http://localhost:8081/app

# Dashboard
curl http://localhost:8081/dashboard
```

### View Logs

```bash
# Backend logs
docker compose logs -f web

# Database logs
docker compose logs -f db

# Frontend logs (if running in background)
tail -f /tmp/tinkerbell-frontend.log
```

## ⚙️ Configuration

### Environment Variables (.env)

Key configuration options in `.env` file:

```env
# Database
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass

# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# API Keys (optional, for advanced features)
OPENAI_API_KEY=your-openai-api-key
META_ACCESS_TOKEN=your-meta-access-token
FACEBOOK_PAGE_ID=your-facebook-page-id
```

### Customization

To customize the application:

1. **Change admin password**:
   - Edit `ADMIN_PASSWORD` in `.env`
   - Restart: `docker compose restart web`

2. **Add allowed hosts** (for external access):
   - Edit `DJANGO_ALLOWED_HOSTS` in `.env`
   - Add your domain/IP
   - Restart: `docker compose restart web`

3. **Change ports**:
   - Backend: Edit `ports` in `docker-compose.yml`
   - Frontend: Edit `port` constant in `tinkerbell-frontend/server.js`

## 🔧 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using the port
lsof -i :8000
lsof -i :8081

# Kill the process
kill -9 <PID>
```

### Issue: Docker Containers Won't Start

```bash
# Check Docker status
docker info

# Clean up and restart
docker compose down -v
docker compose up --build
```

### Issue: Database Connection Errors

```bash
# Check database health
docker compose ps

# View database logs
docker compose logs db

# Reset database (WARNING: deletes all data)
docker compose down -v
docker compose up -d
```

### Issue: Frontend Not Responding

```bash
# Check if Node.js is running
ps aux | grep node

# Check frontend logs
cat /tmp/tinkerbell-frontend.log

# Restart frontend
cd tinkerbell-frontend
node server.js
```

### Issue: SSL Certificate Errors (During Build)

The Dockerfile has been updated to handle SSL certificate issues with PyPI. If you encounter SSL errors:

```bash
# Rebuild with no cache
docker compose build --no-cache
docker compose up -d
```

## 📝 Common Tasks

### Reset Database

```bash
# Stop services
docker compose down

# Remove volumes (deletes all data)
docker compose down -v

# Start fresh
docker compose up -d
```

### Create New Superuser

```bash
docker compose exec web python manage.py createsuperuser --settings=web.settings
```

### Run Django Shell

```bash
docker compose exec web python manage.py shell --settings=web.settings
```

### Run Django Migrations

```bash
docker compose exec web python manage.py migrate --settings=web.settings
```

### Collect Static Files

```bash
docker compose exec web python manage.py collectstatic --settings=web.settings
```

## 🎨 Frontend Routes

The Tinkerbell frontend serves the following pages:

| Route | File | Description |
|-------|------|-------------|
| `/` | `landing.html` | Landing page |
| `/app` | `index.html` | Main application interface |
| `/dashboard` | `dashboard.html` | User dashboard |

## 🔐 Security Notes

1. **Change default passwords** in production
2. **Set `DJANGO_DEBUG=False`** in production
3. **Use HTTPS** in production
4. **Protect sensitive API keys** in `.env`
5. **Don't commit `.env` file** to version control

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Node.js Documentation](https://nodejs.org/docs/)

## 💡 Tips

- Use `docker compose logs -f` to monitor real-time logs
- Keep the `.env` file secure and never commit it
- Use `docker compose restart web` to quickly restart Django after config changes
- The frontend auto-serves static files (CSS, JS, images) from the same directory
- Check browser console for frontend errors
- Check Django logs for backend errors

## 🆘 Need Help?

If you encounter issues:

1. Check the logs (backend and frontend)
2. Verify all prerequisites are installed
3. Ensure ports are not in use
4. Try stopping and restarting services
5. Check the troubleshooting section above

For persistent issues, check the repository issues page or contact the development team.

---

**Happy coding! 🚀**
