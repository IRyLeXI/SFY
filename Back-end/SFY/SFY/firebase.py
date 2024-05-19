import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("F:\Навчання\sfy-firebase-firebase-adminsdk-zu4wv-3557edc9cc.json")
firebase_admin.initialize_app(cred)