# 🎨 Standalone Image Generator

A portable Python script that generates professional marketing images using OpenAI's DALL-E API. Can be used in any workspace or project.

## 🚀 Features

- **DALL-E 3 Integration**: Generate high-quality images using OpenAI's latest model
- **Enhanced Prompts**: Automatically improves prompts for better marketing images
- **Batch Generation**: Generate multiple images in one run
- **Auto Download**: Downloads and saves generated images locally
- **Mock Mode**: Works without API key for testing (uses placeholder images)
- **Portable**: Can be copied to any project and works independently

## 📦 Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key (optional):**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

3. **Or set environment variable directly:**
   ```bash
   export OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Usage

### Basic Usage

```python
from image_generator import ImageGenerator

# Initialize generator
generator = ImageGenerator()

# Generate a single image
result = generator.generate_image(
    description="Professional coffee shop interior with modern design",
    business_name="Urban Coffee Co"
)

print(f"Generated: {result['filename']}")
```

### Batch Generation

```python
# Generate multiple images
image_requests = [
    {
        "description": "Elegant flower arrangement for wedding",
        "business_name": "Floral Dreams"
    },
    {
        "description": "Modern restaurant interior with customers",
        "business_name": "Fine Dining Co"
    }
]

results = generator.generate_multiple_images(image_requests)
generator.save_results_to_json(results)
```

### Command Line Testing

```bash
# Run the built-in test
python image_generator.py
```

## 📁 Output

Generated images are saved to the `generated_images/` folder with unique filenames:
- `generated_1703123456789_abc123.jpg`
- `mock_generated_1703123456789_def456.jpg` (mock mode)

Results are also saved as JSON with metadata:
```json
{
  "success": true,
  "image_url": "https://...",
  "local_path": "./generated_images/generated_1703123456789_abc123.jpg",
  "filename": "generated_1703123456789_abc123.jpg",
  "description": "Professional coffee shop interior",
  "prompt": "Create a professional, high-quality marketing image...",
  "business_name": "Urban Coffee Co",
  "generated_at": "2024-12-21T10:30:45"
}
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required for real generation)

### Constructor Options
```python
generator = ImageGenerator(
    api_key="your_key_here",  # Optional: API key override
    output_dir="my_images"    # Optional: custom output directory
)
```

## 💡 Integration Examples

### Use in Your Project

1. **Copy the files:**
   ```
   your_project/
   ├── image_generator.py
   ├── requirements.txt
   └── .env
   ```

2. **Import and use:**
   ```python
   from image_generator import ImageGenerator
   
   generator = ImageGenerator(output_dir="assets/images")
   result = generator.generate_image("Your image description")
   ```

### API Integration
```python
# Flask example
from flask import Flask, request, jsonify
from image_generator import ImageGenerator

app = Flask(__name__)
generator = ImageGenerator()

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    result = generator.generate_image(
        description=data['description'],
        business_name=data.get('business_name', 'Business')
    )
    return jsonify(result)
```

## 🛠️ Troubleshooting

### No API Key
- Script works in mock mode
- Generates placeholder URLs and filenames
- Useful for testing integration

### API Errors
- Automatically falls back to mock mode
- Check your API key and quota
- Rate limiting adds 2-second delays between requests

### File Permissions
- Ensure write permissions in output directory
- Script creates directory if it doesn't exist

## 📋 Requirements

- Python 3.7+
- `requests` library
- `openai` library (optional, only for real generation)
- OpenAI API key (optional, works without for testing)

## 🎉 Example Output

When you run `python image_generator.py`:

```
🎯 Standalone Image Generator - Test Run
==================================================
✅ OpenAI API key loaded: sk-proj-KUEK4uAkh648...

🧪 Test 1: Single Image Generation
🎨 Generating image: Elegant flower arrangement for a wedding, professional photography
📤 Sending request to OpenAI DALL-E...
📥 Downloading generated image...
✅ Image saved: generated_1703123456789_abc123.jpg
✅ Image generated successfully: generated_1703123456789_abc123.jpg

🧪 Test 2: Multiple Image Generation
🎨 Generating 3 images...

--- Image 1/3 ---
🎨 Generating image: Modern coffee shop interior with customers enjoying coffee
📤 Sending request to OpenAI DALL-E...
📥 Downloading generated image...
✅ Image saved: generated_1703123456790_def456.jpg
⏱️ Waiting 2 seconds between requests...

--- Image 2/3 ---
🎨 Generating image: Professional business team meeting in modern office
📤 Sending request to OpenAI DALL-E...
📥 Downloading generated image...
✅ Image saved: generated_1703123456792_ghi789.jpg
⏱️ Waiting 2 seconds between requests...

--- Image 3/3 ---
🎨 Generating image: Fresh ingredients for healthy cooking, vibrant colors
📤 Sending request to OpenAI DALL-E...
📥 Downloading generated image...
✅ Image saved: generated_1703123456794_jkl012.jpg

✅ Completed: 3/3 images generated successfully
📄 Results saved to: generated_images/generation_results.json

🎉 Test completed!
📁 Check the 'generated_images' folder for generated images
```
