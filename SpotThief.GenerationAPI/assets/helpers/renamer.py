import os
import random
import sys

def deterministic_shuffle_rename(target_dir):
    # Supported formats
    extensions = ('.jpg', '.jpeg', '.png', '.webp', '.svg')
    
    # 1. Get absolute path and list files
    abs_path = os.path.abspath(target_dir)
    if not os.path.exists(abs_path):
        print(f"Error: Directory '{target_dir}' not found.")
        return

    files = [f for f in os.listdir(abs_path) if f.lower().endswith(extensions)]
    
    if not files:
        print(f"No compatible files found in {abs_path}")
        return

    # 2. Shuffle the list to randomize the new indexing
    print(f"Shuffling {len(files)} files in {target_dir}...")
    random.shuffle(files)

    # 3. Rename with padding (001, 002, etc.)
    print("Commencing renaming surgery...")
    
    # We rename to temporary names first to avoid collisions 
    # (e.g., trying to rename a file to a name that already exists in the folder)
    temp_files = []
    for index, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1].lower()
        old_file = os.path.join(abs_path, filename)
        temp_name = os.path.join(abs_path, f"temp_{index}{ext}")
        os.rename(old_file, temp_name)
        temp_files.append((temp_name, f"{index:03d}{ext}"))

    # 4. Final pass to set the clean names
    for temp_path, final_name in temp_files:
        final_path = os.path.join(abs_path, final_name)
        os.rename(temp_path, final_path)
        print(f" ✓ Assigned index: {final_name}")

    print(f"\nDone! Files in {target_dir} are now indexed 001 to {len(files):03d}.")

if __name__ == "__main__":
    # You can run this via: python renamer.py ./assets/backdrops
    if len(sys.argv) > 1:
        deterministic_shuffle_rename(sys.argv[1])
    else:
        print("Usage: python renamer.py <folder_path>")