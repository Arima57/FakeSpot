import os
from PIL import Image

def lanczos_polish_pass(target_size=500):
    extensions = ('.jpg', '.jpeg')
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]
    
    print(f"Applying final Lanczos polish to {len(files)} images...")

    for filename in files:
        try:
            with Image.open(filename) as img:
                # Ensure it's exactly 500x500 one last time
                # Using LANCZOS even at the same resolution helps "de-mush" AI artifacts
                img_polished = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
                
                # Save with high quality to keep the AI detail
                img_polished.save(filename, quality=95, subsampling=0)
                print(f" ✨ {filename}: Polished.")
                
        except Exception as e:
            print(f" ✗ Error polishing {filename}: {e}")

    print("\nFinish! Your backdrops are now AI-enhanced and Lanczos-sharpened.")

if __name__ == "__main__":
    lanczos_polish_pass(500)
