import os
from PIL import Image

def surgical_square_crop():
    # Supported extensions
    extensions = ('.jpg', '.jpeg')
    
    # Get all files in the current directory
    files = [f for f in os.listdir('.') if f.lower().endswith(extensions)]
    
    if not files:
        print("No .jpg or .jpeg files found in this directory.")
        return

    print(f"Found {len(files)} images. Starting surgery...")

    for filename in files:
        try:
            with Image.open(filename) as img:
                width, height = img.size
                
                # Check if already square
                if width == height:
                    print(f" - {filename}: Already square. Skipping.")
                    continue
                
                # Determine the size of the square (shortest side)
                size = min(width, height)
                
                # Calculate coordinates for center crop
                left = (width - size) / 2
                top = (height - size) / 2
                right = (width + size) / 2
                bottom = (height + size) / 2
                
                # Perform the crop
                # The box is a 4-tuple defining (left, upper, right, lower)
                img_cropped = img.crop((left, top, right, bottom))
                
                # Save back to the same filename (Overwrites!)
                img_cropped.save(filename, quality=95, subsampling=0)
                print(f" ✓ {filename}: Cropped to {size}x{size}")
                
        except Exception as e:
            print(f" ✗ Error processing {filename}: {e}")

    print("\nSurgery complete. All images are now squares.")

if __name__ == "__main__":
    surgical_square_crop()
