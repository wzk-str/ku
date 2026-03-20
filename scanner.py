import os

PROTECTED_FILES = {'.gitkeep', 'README.md'}
ALLOWED_EXTENSIONS = {'.txt', '.log'}

def get_file_list(root_path):
    file_list = []
    
    if not os.path.exists(root_path):
        return file_list
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename in PROTECTED_FILES:
                continue
            
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                continue
            
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_path)
            file_list.append({
                'full_path': full_path,
                'relative_path': rel_path,
                'filename': filename
            })
    
    return file_list
