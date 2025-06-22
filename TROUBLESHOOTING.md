# 🛠️ Tinkerbell Troubleshooting Guide

## Issue 1: Images Not Generating or Displaying

### Root Causes:
1. ❌ **Node.js fetch API incompatibility** in imageService.js (FIXED)
2. ❌ **Missing image URL handling** in frontend post cards (FIXED) 
3. ⚠️ **Missing dependencies** or directory permissions

### Solutions Applied:

#### ✅ Fixed imageService.js
- Replaced `fetch()` with Node.js native `https` module
- Added proper URL handling for generated images
- Enhanced error handling for image downloads

#### ✅ Fixed Frontend Display
- Updated `createPostCard()` to show images when available
- Added image preview with error handling
- Enhanced image processing results display

#### ⚠️ Still Need to Check:
```bash
# 1. Ensure all dependencies are installed
cd tinkerbell-backend
npm install

# 2. Check directories exist and have write permissions
mkdir -p uploads generated-images
chmod 755 uploads generated-images

# 3. Test image generation endpoint
curl -X POST http://localhost:3000/api/generate-image \
  -H "Content-Type: application/json" \
  -d '{"description":"a beautiful flower arrangement","businessName":"Test Florarie"}'
```

---

## Issue 2: Facebook Posting Not Working

### Root Causes:
1. ✅ **Environment configured** - OpenAI and Planable credentials are set
2. ⚠️ **Planable API token may be invalid** or expired
3. ⚠️ **Facebook Page not properly connected** to Planable

### Current Configuration (.env):
```bash
PLANABLE_ACCESS_TOKEN=EAAX8ZBs... (appears to be set)
FACEBOOK_PAGE_ID=713473578508242 (appears to be set)  
AUTO_POST_ENABLED=true (enabled)
```

### Verification Steps:

#### 1. Test Planable API Connection
```bash
# Test if Planable token is valid
curl -H "Authorization: Bearer EAAX8ZBs..." \
  https://api.planable.io/v1/workspaces
```

#### 2. Check Facebook Page Connection
- Log into https://app.planable.io
- Go to Settings → Social Accounts
- Verify Facebook page is connected and has posting permissions
- Check if Facebook page ID matches: `713473578508242`

#### 3. Facebook App Requirements
You'll need:
- **Facebook App** (create at developers.facebook.com)
- **App Review** for pages_manage_posts permission
- **Page Access Token** (not App Secret directly)
- **Webhook configuration** for real-time updates

#### 4. Alternative: Use Mock Mode for Testing
```bash
# In .env file, disable auto-posting to test without Facebook
AUTO_POST_ENABLED=false
```

---

## 🚀 Quick Fix Commands

### Restart Backend with Fixes:
```bash
cd tinkerbell-backend
npm install  # Ensure all dependencies
node server.js  # Should show "Image directories initialized"
```

### Test Image Upload:
```bash
# Upload a test image
curl -X POST http://localhost:3000/api/upload-images \
  -F "images=@path/to/your/image.jpg"
```

### Test Campaign with Images:
```bash
# Create campaign with image generation
curl -X POST http://localhost:3000/api/schedule-campaign-with-images \
  -H "Content-Type: application/json" \
  -d '{
    "businessData": {"businessName": "Test Business"},
    "confirmedPersonas": [{"name": "Test Persona"}],
    "generateMissingImages": true
  }'
```

---

## 📞 Expected Results After Fixes:

### Images:
- ✅ Uploaded images show previews immediately
- ✅ Generated images appear in post cards
- ✅ Image count shows correctly ("X uploaded associated images")
- ✅ Mock images work when OpenAI unavailable

### Facebook Posting:
- ✅ Planable workspace created successfully
- ✅ Posts scheduled as drafts in Planable
- ⚠️ Auto-posting depends on proper Facebook app setup
- ✅ Graceful fallback to manual review when auto-post disabled

---

## 🔍 Debug Commands:

```bash
# Check server logs
tail -f tinkerbell-backend/debug.log

# Test specific endpoints
curl http://localhost:3000/health
curl -X POST http://localhost:3000/api/create-personas -d '{"businessName":"Test"}'

# Check uploaded files
ls -la tinkerbell-backend/uploads/
ls -la tinkerbell-backend/generated-images/
```
