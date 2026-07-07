import os
import shutil

src_dir = r"C:\Users\vansh\.gemini\antigravity\brain\ad505ede-7706-42c4-a8b9-a0b4692336ba"
dest_dir = r"D:\UPSS\frontend\public\images"

os.makedirs(dest_dir, exist_ok=True)

files = {
    "media__1783254476798.jpg": "Techstack.jpeg",
    "media__1783254476801.jpg": "workflow.jpeg",
    "media__1783254476806.jpg": "System Architecture.jpeg"
}

for src_name, dest_name in files.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_name} to {dest_name}")
    else:
        print(f"Not found: {src_path}")
