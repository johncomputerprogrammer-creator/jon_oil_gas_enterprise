import os

def show_structure(path, indent=0):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        print('    ' * indent + '|-- ' + item)
        if os.path.isdir(item_path):
            show_structure(item_path, indent + 1)

project_path = r"C:\Users\USER\OneDrive\Documents\jon_oil_gas_enterprise"
print(f"Project structure for: {project_path}\n")
show_structure(project_path)
