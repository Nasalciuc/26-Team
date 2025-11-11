# PAȘII URMĂTORI - Ești în aplicația "team 26"
# =============================================

## 🎯 SITUAȚIA ACTUALĂ:
✅ Ești în dashboard-ul aplicației "team 26"
✅ Aplicația este "Unpublished" (perfect pentru dezvoltare)
✅ Ai acces la toate setările

## 📋 PAȘII URMĂTORI (în ordinea exactă):

### PASUL 1: Obține App ID și App Secret
📍 **UNDE:** În meniul din stânga → "App settings" (cu iconița roții)
🔧 **CE FACI:**
1. Click pe "App settings" din meniul stâng
2. Click pe "Basic" 
3. Vei vedea:
   - **App ID**: (numărul de sus - copiază-l)
   - **App Secret**: Click "Show" → copiază valoarea

### PASUL 2: Adaugă Facebook Login
📍 **UNDE:** Înapoi la Dashboard → butonul verde "Add Product"
🔧 **CE FACI:**
1. Scroll pe pagina principală și caută "Add Product" 
2. Găsește "Facebook Login" → Click "Set Up"
3. Alege "Web" ca platformă
4. Site URL: `http://localhost:8000`
5. Salvează

### PASUL 3: Adaugă Pages API  
📍 **UNDE:** Din nou "Add Product"
🔧 **CE FACI:**
1. Caută "Facebook Pages API" → Click "Set Up"
2. Configurează permisiunile pentru pages
3. Salvează

### PASUL 4: Generează Access Token
📍 **UNDE:** Tools → Graph API Explorer (link în header-ul paginii)
🔧 **CE FACI:**
1. Selectează aplicația "team 26" din dropdown
2. Click "Generate Access Token"
3. Selectează permisiunile:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
4. Copiază token-ul generat

### PASUL 5: Obține Page ID
📍 **UNDE:** În Graph API Explorer
🔧 **CE FACI:**
1. Schimbă request-ul la: `/me/accounts`
2. Click "Submit"
3. Găsește pagina pe care vrei să postezi
4. Copiază "id" pentru pagină

## 🚀 ÎNCEPE CU:
**Click pe "App settings" din meniul stâng pentru App ID și Secret!**

Îți voi ghida pas cu pas când ajungi la fiecare secțiune!