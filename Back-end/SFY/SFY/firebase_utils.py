from firebase_admin import storage

def upload_user_picture_firebase(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"profile_pictures/{file.name}")
    blob.upload_from_file(file)

    return blob.public_url


def upload_song_audio_firebase(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"songs/audio/{file.name}")
    blob.upload_from_file(file)
    return blob.public_url


def upload_song_picture_firebase(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"songs/pictures/{file.name}")
    blob.upload_from_file(file)
    return blob.public_url


def upload_album_picture_firebase(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"albums_pictures/{file.name}")
    blob.upload_from_file(file)

    return blob.public_url


def upload_playlist_picture_firebase(file):
    bucket = storage.bucket()
    blob = bucket.blob(f"playlists_pictures/{file.name}")
    blob.upload_from_file(file)

    return blob.public_url