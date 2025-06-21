# Django + PostgreSQL Docker Project

Acest proiect conține o aplicație Django configurată să ruleze cu PostgreSQL într-un mediu Docker.

## 📁 Structura proiectului

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
└── myproject/         ← proiectul Django
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── asgi.py
    └── management/
        └── commands/
            └── wait_for_db.py
```

## 🚀 Instrucțiuni de pornire

### 1. Configurare automată a mediului

```bash
# Rulează scriptul de setup (recomandat)
./setup-env.sh

# SAU copiază manual
cp env.example .env
```

### 2. Pornește totul cu o singură comandă!

```bash
# Construiește și pornește containerele
docker-compose up --build
```

**Asta e tot!** 🎉

Scriptul de startup va:
- ✅ Aștepta ca baza de date să fie gata
- ✅ Rula migrările automat
- ✅ Crea un superuser din variabilele de mediu
- ✅ Porni serverul Django

## 🌐 Accesare aplicație

- **Aplicație Django**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
  - **Username**: admin (configurabil în .env)
  - **Password**: admin123 (configurabil în .env)

## 🔧 Configurare variabile de mediu

### Variabile disponibile în `.env`:

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
```

### Personalizare:

1. **Schimbă parola admin**:
   ```env
   ADMIN_PASSWORD=your_secure_password
   ```

2. **Schimbă numele bazei de date**:
   ```env
   POSTGRES_DB=your_database_name
   ```

3. **Dezactivează debug mode**:
   ```env
   DJANGO_DEBUG=False
   ```

## 🛠️ Comenzi utile

### Rulare în background
```bash
docker-compose up -d --build
```

### Oprire servicii
```bash
docker-compose down
```

### Oprire și ștergere volume-uri
```bash
docker-compose down -v
```

### Verificare log-uri
```bash
docker-compose logs web
docker-compose logs db
```

### Accesare shell Django
```bash
docker-compose run web python manage.py shell
```

### Creare superuser manual
```bash
docker-compose run web python manage.py createsuperuser
```

### Regenerare fișier .env
```bash
./setup-env.sh
```

## 📊 Baza de date

- **Tip**: PostgreSQL 15
- **Host**: localhost:5432
- **Database**: django_db (configurabil)
- **User**: django_user (configurabil)
- **Password**: django_pass (configurabil)

## 📝 Note importante

1. Asigură-te că Docker și Docker Compose sunt instalate și rulează
2. Portul 8000 trebuie să fie liber pentru aplicația Django
3. Portul 5432 trebuie să fie liber pentru PostgreSQL
4. Prima rulare poate dura mai mult din cauza descărcării imaginilor Docker
5. Superuser-ul se creează automat la prima rulare din variabilele de mediu
6. Toate setările sunt configurabile prin fișierul `.env`

## 🐛 Depanare

### Dacă Docker nu pornește
```bash
# Verifică statusul Docker
docker --version
docker-compose --version

# Repornește Docker Desktop
```

### Dacă porturile sunt ocupate
```bash
# Verifică ce rulează pe porturi
lsof -i :8000
lsof -i :5432

# Modifică porturile în docker-compose.yml dacă e necesar
```

### Dacă migrările eșuează
```bash
# Șterge volume-urile și începe din nou
docker-compose down -v
docker-compose up --build
```

### Dacă vrei să resetezi totul
```bash
# Oprește și șterge tot
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Dacă ai probleme cu .env
```bash
# Regenerază fișierul .env
./setup-env.sh
``` 