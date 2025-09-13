import os
import shutil

# Define paths
project_dir = os.getcwd()
templates_static_path = os.path.join(project_dir, "templates", "static")
new_static_path = os.path.join(project_dir, "static")

print("🔄 Fixing your static folder structure...")

# Check if templates/static exists
if not os.path.exists(templates_static_path):
    print("✅ Your static folder is already in the right place. No changes needed.")
else:
    # Create new static folder if it doesn't exist
    if not os.path.exists(new_static_path):
        os.makedirs(new_static_path)
        print(f"📂 Created new folder: {new_static_path}")

    # Move everything from templates/static to the new static folder
    for item in os.listdir(templates_static_path):
        source = os.path.join(templates_static_path, item)
        destination = os.path.join(new_static_path, item)

        # If destination already exists, skip to avoid overwriting
        if os.path.exists(destination):
            print(f"⚠️ Skipping {item} (already exists in static/)")
        else:
            shutil.move(source, destination)
            print(f"✅ Moved {item} → static/")

    # Remove the empty templates/static folder
    try:
        os.rmdir(templates_static_path)
        print("🗑️ Removed old templates/static folder.")
    except OSError:
        print("⚠️ Could not remove templates/static (not empty).")

print("🎯 Done! Your static folder is now fixed.")
print("💡 Next Step: Update your HTML to use this format → {{ url_for('static', filename='images/your_image.jpg') }}")
