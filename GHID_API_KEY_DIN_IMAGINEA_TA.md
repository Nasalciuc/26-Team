# Cum să obții Meta API Key din imaginea ta
# ===========================================

## SITUAȚIA ACTUALĂ (din imaginea ta):
✅ Ai deja cont Meta for Developers activ
✅ Ai aplicația "team 26" creată (perfectă pentru Market Spark)
✅ Ești pe dashboard-ul corect

## PAȘII PENTRU OBȚINEREA API KEY-ULUI:

### PASUL 1: Accesează aplicația "team 26"
1. Click pe aplicația "team 26" din dashboard
2. Vei intra în configurarea aplicației

### PASUL 2: Obține App ID și App Secret
1. În aplicația "team 26", mergi la Settings → Basic
2. Copiază:
   - App ID: (numărul de sus)
   - App Secret: Click "Show" și copiază valoarea

### PASUL 3: Adaugă Facebook Login (dacă nu e deja)
1. În meniul din stânga, click pe "Add Product" 
2. Găsește "Facebook Login" → Click "Set Up"
3. Selectează "Web" ca platformă
4. Adaugă URL-ul: http://localhost:8000

### PASUL 4: Adaugă Pages API (pentru postări)
1. Click din nou pe "Add Product"
2. Găsește "Facebook Pages API" → Click "Set Up"
3. Configurează permisiunile pentru pagini

### PASUL 5: Generează Access Token
1. Mergi la Tools → Graph API Explorer (link în meniul de sus)
2. Selectează aplicația "team 26" din dropdown
3. Click pe "Generate Access Token"
4. Selectează permisiunile:
   - pages_manage_posts
   - pages_read_engagement  
   - pages_show_list
5. Copiază token-ul generat

### PASUL 6: Obține Page ID
1. În Graph API Explorer, cu token-ul de la pasul 5
2. Schimbă request-ul la: /me/accounts
3. Click "Submit"
4. Găsește pagina pe care vrei să postezi
5. Copiază "id" și "access_token" pentru pagina respectivă

## CONFIGURARE ÎN MARKET SPARK:

Editează fișierul .env cu valorile obținute:

```env
# Meta API Keys pentru aplicația "team 26"
META_ACCESS_TOKEN=EAAY... # Page Access Token din pasul 6
FACEBOOK_PAGE_ID=123456789 # Page ID din pasul 6  
META_APP_SECRET=abc123def456 # App Secret din pasul 2
```

## LINK-URI RAPIDE:
- Dashboard aplicația ta: https://developers.facebook.com/apps/
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Settings aplicația: https://developers.facebook.com/apps/[APP_ID]/settings/basic/

## TESTARE:
După configurare:
1. Restart Django server
2. Încearcă o postare prin Market Spark
3. Verifică pe pagina ta de Facebook

🔥 **AVANTAJ**: Ai deja aplicația creată, deci doar trebuie să extragi cheile!