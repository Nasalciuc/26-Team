# NOD1 - Universal Super Scraper

## Descriere
NOD1 este un scraper universal pentru extragerea informațiilor complete de pe site-urile web. Acesta folosește DrissionPage pentru a accesa și analiza paginile web, extragând o gamă largă de date structurate.

## Funcționalități

### 🔍 Extragerea Datelor
- **Meta Tags**: Toate meta tag-urile din `<head>`
- **Titluri**: H1-H6 headings cu conținutul lor
- **Paragrafe**: Toate paragrafele din pagină
- **Linkuri**: Toate linkurile cu text și URL-uri
- **Imagini**: Toate imaginile cu src și alt text
- **Butoane**: Butoane și input-uri cu text
- **Liste**: Listele ordonate și neordonate
- **Tabele**: Structura tabelelor cu date
- **Formulare**: Formulare cu action și input-uri
- **Scripts**: Script-uri externe și inline
- **CSS**: Fișiere CSS și stiluri
- **Div-uri importante**: Div-uri cu clase CSS
- **Span-uri**: Elemente span cu conținut
- **Informații de contact**: Email-uri și telefoane
- **Rețele sociale**: Linkuri către platforme sociale
- **Informații companie**: Titlu și descriere
- **Statistici**: Numere și procente din text
- **Clase CSS**: Toate clasele CSS folosite
- **ID-uri**: Toate ID-urile elementelor

### 📊 Export de Date
- **JSON**: Export complet în format JSON
- **CSV**: Export structurat în format CSV
- **Timestamp**: Fiecare export include timestamp

## Instalare

```bash
pip install -r requirements.txt
```

## Utilizare

### Rulare directă
```bash
python NOD1.py
```

### Import în alte proiecte
```python
from NOD1 import UniversalSuperScraper

scraper = UniversalSuperScraper()
data = scraper.extract_all_data("https://example.com")
```

## Exemplu de Output

```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "scraped_at": "2025-06-21T22:19:53.935536",
  "page_title": "Example Domain",
  "meta_tags": {
    "description": "Example domain for testing",
    "viewport": "width=device-width, initial-scale=1"
  },
  "headings": {
    "h1": ["Example Domain"],
    "h2": ["Further Reading"]
  },
  "paragraphs": [
    "This domain is for use in illustrative examples in documents."
  ],
  "links": [
    {
      "text": "More information...",
      "url": "https://www.iana.org/domains/example"
    }
  ],
  "images": [],
  "contact_info": {
    "emails": ["contact@example.com"]
  },
  "social_media": {},
  "statistics": ["100%", "2025"]
}
```

## Integrare cu Django

NOD1 este integrat în aplicația Django pentru:
- Scraping automat prin interfața web
- Salvare în baza de date PostgreSQL
- Export prin API-uri web
- Interfață Bootstrap pentru utilizatori

## Caracteristici Tehnice

- **Browser Engine**: DrissionPage pentru rendering JavaScript
- **Parsing HTML**: BeautifulSoup pentru analiza DOM
- **Regex**: Pentru extragerea pattern-urilor (email, telefon, etc.)
- **URL Processing**: Pentru normalizarea linkurilor relative
- **Error Handling**: Gestionarea erorilor de conexiune și parsing
- **Encoding**: Suport pentru caractere Unicode

## Limitări

- Necesită DrissionPage instalat pentru funcționalitate completă
- Poate fi lent pentru site-uri mari
- Respectă robots.txt și rate limiting
- Nu poate accesa conținut din iframe-uri externe

## Autor
Team 26 - Proiect de scraping universal 