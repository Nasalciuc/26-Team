# 🧪 Testing Guide for Image Upload & Facebook Posting

## 📁 Created Test Folders

### 1. **Facebook Posting Test** (`facebook-posting-test/`)
- **Purpose**: Test direct Facebook posting via Planable API
- **File**: `test-facebook-post.js` - Comprehensive Facebook posting test
- **What it tests**:
  - ✅ Planable API connectivity
  - ✅ Workspace creation
  - ✅ Post creation and scheduling
  - ✅ Facebook publishing with your credentials

### 2. **Image Upload Test** (`image-upload-test/`)
- **Purpose**: Test image analysis and matching
- **File**: `test-image-upload.js` - Image analysis with gpt-4o
- **What it tests**:
  - ✅ Image upload detection
  - ✅ gpt-4o vision analysis
  - ✅ Image-to-post matching logic

### 3. **Backend Simple Tests** (`tinkerbell-backend/`)
- **File**: `test-my-uploaded-images.js` - Analyze your car + salon images
- **File**: `test-facebook-simple.js` - Simple Facebook posting test

## 🔧 Your Current Issues

### ❌ **Issue 1: Images Not Showing in Posts**
**Root Cause**: Image matching algorithm may not be finding suitable matches

**Your uploaded images**:
- `images-1750551440736-580134369.jpg` (56KB - likely salon)
- `images-1750551445410-128485223.jpg` (5.4MB - likely car)

**Possible reasons**:
1. Images analyzed but keywords don't match post content
2. Confidence threshold too high
3. gpt-4o analysis not finding relevant business keywords

### ❌ **Issue 2: No Facebook Posts Created**
**Root Cause**: Planable API integration issues

**Your configuration**:
- ✅ Planable Token: Set
- ✅ Facebook Page ID: 713473578508242
- ✅ Facebook App ID: 1510959450278764
- ✅ Facebook App Secret: Set

**Possible issues**:
1. Network connectivity to app.planable.io
2. Facebook app not properly connected to Planable
3. Token permissions insufficient
4. Facebook page not linked to the app

## 🚀 How to Test

### **Test Image Analysis**:
```bash
cd "c:\Users\Phantom\Documents\Projects\Tinkerbell\tinkerbell-backend"
node test-my-uploaded-images.js
```

### **Test Facebook Posting**:
```bash
cd "c:\Users\Phantom\Documents\Projects\Tinkerbell\tinkerbell-backend"
node test-facebook-simple.js
```

### **Test via Frontend**:
1. Open: http://localhost:8080
2. Upload your car and salon images again
3. Create a campaign
4. Check if images appear in posts
5. Check if posts get scheduled to Facebook

## 🔍 Debugging Steps

### **For Image Issues**:
1. Run `test-my-uploaded-images.js` to see gpt-4o analysis
2. Check if keywords match your business type
3. Verify image file formats and sizes
4. Check upload timestamp vs campaign creation

### **For Facebook Issues**:
1. Run `test-facebook-simple.js` for API connectivity
2. Check Planable dashboard: https://app.planable.io
3. Verify Facebook app settings at developers.facebook.com
4. Test token validity manually

## 📊 Expected Outcomes

### **Working Image Upload**:
- gpt-4o analyzes images correctly
- Identifies car vs salon content
- Matches images to appropriate posts
- Shows images in campaign preview

### **Working Facebook Posting**:
- Creates Planable workspace
- Schedules posts successfully
- Publishes to Facebook page
- Returns Facebook post IDs

## 🎯 Next Steps

1. **Run the tests** to identify specific failure points
2. **Check logs** for error messages
3. **Verify credentials** are correct and active
4. **Test manually** via Planable dashboard
5. **Update matching logic** if needed

Both test environments are ready to help you debug the issues! 🚀
