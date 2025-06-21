# Django + PostgreSQL Docker Project

Acest proiect conține o aplicație Django configurată să ruleze cu PostgreSQL într-un mediu Docker.

## 📁 Structura proiectului

```
team26/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── env.example
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

### 1. Configurare inițială

```bash
# Copiază fișierul de configurare
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
- ✅ Crea un superuser (admin/admin123) dacă nu există
- ✅ Porni serverul Django

## 🌐 Accesare aplicație

- **Aplicație Django**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
  - **Username**: admin
  - **Password**: admin123

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

### Creare superuser manual (dacă e necesar)
```bash
docker-compose run web python manage.py createsuperuser
```

## 📊 Baza de date

- **Tip**: PostgreSQL 15
- **Host**: localhost:5432
- **Database**: django_db
- **User**: django_user
- **Password**: django_pass

## 🔧 Configurare

### Variabile de mediu (.env)
```env
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
```

### Dependințe Python (requirements.txt)
- Django>=4.2
- psycopg2-binary>=2.9

## 📝 Note importante

1. Asigură-te că Docker și Docker Compose sunt instalate și rulează
2. Portul 8000 trebuie să fie liber pentru aplicația Django
3. Portul 5432 trebuie să fie liber pentru PostgreSQL
4. Prima rulare poate dura mai mult din cauza descărcării imaginilor Docker
5. Superuser-ul se creează automat la prima rulare

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