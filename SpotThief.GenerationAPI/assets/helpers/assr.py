import os
import time
import requests
import cloudinary
import cloudinary.uploader

# Your credentials
cloudinary.config(
    cloud_name = "dhkvzsgng", 
    api_key = "341381951891554",
    api_secret = "pvWHXvy8y7PqxVJUTgiLt2eq0DM"
)

def ai_upscale_to_500():
    extensions = ('.jpg', '.jpeg')
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]
    
    print(f"🚀 Starting AI Super-Resolution for {len(files)} images...")

    for filename in files:
        try:
            print(f"Upscaling: {filename}...")
            
            # 1. Upload with High-Detail AI Transformations
            # e_upscale: Uses generative AI to rebuild resolution
            # e_improve: Fixes lighting and colors (perfect for that neon/anime pop)
            # w_500, h_500, c_fill: Forces the exact target size we need
            upload_result = cloudinary.uploader.upload(
                filename,
                transformation=[
                    {"effect": "upscale"},
                    {"effect": "improve"},
                    {"width": 500, "height": 500, "crop": "fill"},
                    {"quality": "auto:best"}
                ]
            )
            
            # 2. Get the URL of the enhanced image
            enhanced_url = upload_result['secure_url']
            
            # 3. Save it back to your local folder
            response = requests.get(enhanced_url)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f" ✓ {filename}: Now a High-Def 500x500.")
            
            # 4. Stay within Free Tier limits (delay slightly)
            time.sleep(3) 

        except Exception as e:
            print(f" ✗ Error on {filename}: {e}")

    print("\n✨ All images have been AI-enhanced to 500x500.")

if __name__ == "__main__":
    ai_upscale_to_500()
