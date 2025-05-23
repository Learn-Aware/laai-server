import os
from fastapi import UploadFile

def save_uploaded_file(file: UploadFile, upload_dir="uploads"):
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path
