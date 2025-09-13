import os
import zipfile
import requests

# Folder for images
images_folder = os.path.join(os.getcwd(), "static", "images")
os.makedirs(images_folder, exist_ok=True)

# Image URLs
images = {
    "gas12.jpg": "https://i.ibb.co/gM5G7gF/gas12.jpg",
    "engineoil5l.jpg": "https://i.ibb.co/ykV2f7T/engineoil5l.jpg",
    "diesel50l.jpg": "https://i.ibb.co/VLkW5cY/diesel50l.jpg",
    "gasburner.jpg": "https://i.ibb.co/JR58vQq/gasburner.jpg",
    "generator3_5kva.jpg": "https://i.ibb.co/x8Zt3gC/generator3-5kva.jpg"
}

# Download images
for name, url in images.items():
    r = requests.get(url)
    path = os.path.join(images_folder, name)
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"Downloaded {name}")

# Create ZIP
zip_path = os.path.join(os.getcwd(), "static", "product_images.zip")
with zipfile.ZipFile(zip_path, "w") as zipf:
    for name in images.keys():
        zipf.write(os.path.join(images_folder, name), name)

print(f"✅ ZIP created at {zip_path}")
