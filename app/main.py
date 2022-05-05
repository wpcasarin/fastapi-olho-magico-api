import base64
from io import BytesIO

import face_recognition as fr
import numpy as np
from fastapi import FastAPI, File, Form, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app.firebase import db
from app.util import optimize_img

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'Api running...'}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(response: Response, name: str = Form(...), phone: str = Form(...), user_id: str = Form(...), file: UploadFile = File(...)):
    """
    Register new contact
    """
    img_bytes = await file.read()
    img_pillow = Image.open(BytesIO(img_bytes))
    img_bytes = optimize_img(img_pillow)
    img_optimized = Image.open(BytesIO(img_bytes))
    unknown_img = np.asarray(img_optimized)
    if (fr.face_locations(unknown_img)):
        contact_img = base64.b64encode(img_bytes)
        data = {'name': name, 'phone': phone, 'image': str(contact_img)[
            2:-1]}
        db.collection('users').document(
            user_id).collection('contacts').add(data)
        return {'message': f'Contato {name} adicionado com sucesso.'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'message': f'Algo deu errado.'}
