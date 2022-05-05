import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore

# load .env
load_dotenv()
# firebase connection
firebase_admin.initialize_app()
db = firestore.client()
