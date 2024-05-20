from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import io

def authenticate(fileId):
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )

    creds = flow.run_local_server(port=50745)

    service = build('drive', 'v3', credentials=creds)

    request = service.files().get(supportsAllDrives=True, fileId=fileId)
    file_data = request.execute()
    print(f"Name: {file_data['name']}, MIME type: {file_data['mimeType']}")

    request = service.files().get_media(supportsAllDrives=True, fileId=fileId)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    with open(file_data['name'], 'wb') as f:
        fh.seek(0)
        f.write(fh.read())
    
    return file_data['name']

authenticate()