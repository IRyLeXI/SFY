from firebase_admin import storage

def upload_to_firebase_storage(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"profile_pictures/{file.name}")
    blob.upload_from_file(file)

    return blob.public_url