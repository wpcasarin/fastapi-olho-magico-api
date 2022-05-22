import uuid
from dataclasses import dataclass
from io import BytesIO

import face_recognition as fr
import numpy as np
from fastapi import FastAPI, File, Form, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from firebase import db
from util import optimize_img

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)


@dataclass
class UserData:
    """Firebase user data"""
    id: str


@app.get('/')
async def root():
    return {'message': 'Api está funcionando...'}


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(response: Response, name: str = Form(...), phone: str = Form(...), user_id: str = Form(...), file: UploadFile = File(...)):
    """
    Register new contact
    """
    img_bytes = await file.read()
    img_pillow = Image.open(BytesIO(img_bytes))
    img_bytes_optimized = optimize_img(img_pillow)
    img_pillow_optimized = Image.open(BytesIO(img_bytes_optimized))
    unknown_img = np.asarray(img_pillow_optimized)
    if (fr.face_locations(unknown_img)):
        data = {'id': str(uuid.uuid4()), 'name': name, 'phone': phone,
                'image': img_bytes_optimized}
        db.collection('users').document(
            user_id).collection('contacts').add(data)
        return {'message': f'{name} foi adicionado a lista de contatos'}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {'message': f'Imagem inválida, tire outra foto.'}


@app.post('/contacts')
async def contacts(user: UserData):
    """
    List all contacts
    """
    contact_list = []
    contacts = db.collection('users').document(
        user.id).collection('contacts').get()
    if contacts:
        for contact in contacts:
            current = contact.to_dict()
            contact_data = {
                'id': current['id'], 'name': current['name'], 'phone': current['phone']}
            contact_list.append(contact_data)
        return contact_list
    return {'message': 'Erro ao listar contatos'}
