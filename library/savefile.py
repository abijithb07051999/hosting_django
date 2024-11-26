from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

url = 'http://localhost:8000/media'
def saveFile(path  : str ,file : InMemoryUploadedFile) -> str:
    fs=FileSystemStorage()
    half_image_path= fs.save(f'{path}/{file}',file)
    full_image_path=  f'{url}/{half_image_path}'
    return full_image_path

