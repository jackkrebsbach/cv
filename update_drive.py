import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load credentials
creds_json = os.environ['GOOGLE_DRIVE_CREDENTIALS']
creds_dict = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(creds_dict)

# Create Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# Search for the file
response = drive_service.files().list(
    q="name='cv.pdf' and 'root' in parents",
    spaces='drive',
    fields='files(id, name, parents, webViewLink)'
).execute()

files = response.get('files', [])

if not files:
    print('File not found. Creating new file.')
    file_metadata = {
        'name': 'cv.pdf',
        'parents': ['root']  # This ensures the file is created in the root of My Drive
    }
    media = MediaFileUpload('cv.pdf', resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name, parents, webViewLink').execute()
    print(f'File created:')
    print(f'  ID: {file.get("id")}')
    print(f'  Name: {file.get("name")}')
    print(f'  Parent folder: {file.get("parents")}')
    print(f'  Web view link: {file.get("webViewLink")}')
    
    # Share the file with your personal Google account
    your_email = 'jack.krebsbach@colorado.edu'  
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': your_email
    }
    drive_service.permissions().create(fileId=file.get('id'), body=permission).execute()
    print(f'File shared with {your_email}')
else:
    file_id = files[0]['id']
    print(f'Updating existing file:')
    print(f'  ID: {file_id}')
    print(f'  Name: {files[0].get("name")}')
    print(f'  Parent folder: {files[0].get("parents")}')
    print(f'  Web view link: {files[0].get("webViewLink")}')
    media = MediaFileUpload('cv.pdf', resumable=True)
    updated_file = drive_service.files().update(
        fileId=file_id,
        media_body=media
    ).execute()
    print(f'File updated successfully.')
