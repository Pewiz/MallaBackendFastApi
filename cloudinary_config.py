import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv
import os
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

async def upload_image(file: UploadFile):
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder = "malla_carreras",
            allowed_formats= ["jpg", "png", "jpeg", "webp"]
        )
        return result["secure_url"]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {str(e)}")
    