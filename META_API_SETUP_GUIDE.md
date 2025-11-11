# Cum să obții Meta API Key pentru Market Spark
# ===============================================

## PASUL 1: Creează un cont Meta for Developers
1. Mergi la: https://developers.facebook.com/
2. Conectează-te cu contul tău de Facebook
3. Acceptă termenii și condițiile pentru developers

## PASUL 2: Creează o aplicație Meta
1. Click pe "My Apps" în meniul de sus
2. Click pe "Create App"
3. Alege "Business" ca tip de aplicație
4. Completează:
   - App Name: "Market Spark" (sau numele pe care îl preferi)
   - App Contact Email: emailul tău
   - Business Account: (opțional, poți să sari)
5. Click "Create App"

## PASUL 3: Configurează produsele necesare
În dashboard-ul aplicației tale:

### A. Facebook Login
1. Click pe "Add Product"
2. Găsește "Facebook Login" și click "Set Up"
3. Alege "Web" ca platformă
4. Site URL: http://localhost:8000 (pentru dezvoltare)

### B. Facebook Pages API
1. Click pe "Add Product"
2. Găsește "Facebook Pages API" și click "Set Up"
3. Configurează permisiunile pentru pages

## PASUL 4: Obține Access Token-ul
1. Mergi la Tools > Graph API Explorer
2. Selectează aplicația ta din dropdown
3. Generează un User Access Token cu permisiunile:
   - pages_manage_posts
   - pages_read_engagement
   - pages_show_list
4. Copiază token-ul generat

## PASUL 5: Obține Page ID
1. În Graph API Explorer, folosește token-ul de la pasul 4
2. Fă o cerere GET la: /me/accounts
3. Găsește pagina pe care vrei să postezi
4. Copiază "id" și "access_token" pentru pagina respectivă

## PASUL 6: Obține App Secret
1. În dashboard-ul aplicației, mergi la Settings > Basic
2. Găsește "App Secret" 
3. Click "Show" și copiază valoarea

## CONFIGURARE ÎN MARKET SPARK:

Editează fișierul .env cu valorile obținute:

```
# Meta API Keys (înlocuiește cu valorile tale reale)
META_ACCESS_TOKEN=EAAxxxxxx...  # Page Access Token din pasul 5
FACEBOOK_PAGE_ID=123456789      # Page ID din pasul 5  
META_APP_SECRET=abc123def456    # App Secret din pasul 6
```

## VERIFICARE CONFIGURARE:
După ce ai configurat cheile în .env:
1. Restart servrul Django
2. Încearcă să postezi ceva pe Facebook prin Market Spark
3. Verifică în Facebook Page-ul tău dacă postarea a apărut

## LIMITĂRI ÎN DEZVOLTARE:
- Token-urile de test expiră în 2 luni
- Pentru producție, vei avea nevoie de App Review de la Meta
- Unele funcții necesită verificare de business

## LINKURI UTILE:
- Meta for Developers: https://developers.facebook.com/
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Documentație Pages API: https://developers.facebook.com/docs/pages-api/

## TROUBLESHOOTING:
- Dacă token-ul expiră: generează unul nou în Graph API Explorer
- Dacă postarea nu funcționează: verifică permisiunile token-ului
- Pentru producție: aplică pentru App Review la Meta