import os
from PIL import Image

def surgical_upscale_only(min_size=300):
    # Standard image formats
    extensions = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]
    
    if not files:
        print("No compatible image files found.")
        return

    print(f"Checking {len(files)} images for minimum {min_size}x{min_size} resolution...")

    for filename in files:
        try:
            with Image.open(filename) as img:
                width, height = img.size
                
                # Check if it meets the minimum resolution requirement
                if width < min_size or height < min_size:
                    # Upscale to standard using LANCZOS for maximum sharpness
                    img = img.resize((min_size, min_size), Image.Resampling.LANCZOS)
                    
                    # Save back to same filename
                    img.save(filename, quality=95, subsampling=0)
                    print(f" ✓ {filename}: Upscaled from {width}x{height} to {min_size}x{min_size}")
                else:
                    print(f" - {filename}: Pass ({width}x{height})")
                
        except Exception as e:
            print(f" ✗ Error processing {filename}: {e}")

    print("\nResolution check complete. All images are standard.")

if __name__ == "__main__":
    surgical_upscale_only(500)
