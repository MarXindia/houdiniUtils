# ===================== Import necessary libraries =====================================
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# =======================================================================================

class GDriveUtils:

    def __init__(self, client_secret:str, token:str, file_to_upload:str, file_in_folder='Default', port=8080):

        self.port = port
        self.client_secret = client_secret
        self.token = token
        self.file_path = file_to_upload
        self.file_in_folder = file_in_folder

    def gAuthenticate(self):
        SCOPE = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists(self.token):
            creds = Credentials.from_authorized_user_file(self.token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret, SCOPE)
                creds = flow.run_local_server(port=self.port)
            # Save the credentials for the next run
            with open(self.token, 'w') as token:
                token.write(creds.to_json())
        return creds

    # Upload file function save the file in desired folder
    # local_path variable allows to save the file as just the file name or as complete local -
    # path (which later can be used to generate whole hierarchy while downloading it back)

    def upload_file(self,local_path=False,mime_type='application/octet-stream'):
        import os
        file_name = self.file_path
        creds = self.gAuthenticate()
        drive_service = build('drive', 'v3', credentials=creds)
        folder_id = self._create_folder(drive_service)

        if not local_path:
            file_name = os.path.basename(file_name)

        file_metadata = {
            'name': file_name,  # Name of the file in Google Drive
            'mimeType': mime_type,
            'parents': [folder_id]  # ID of the parent folder
        }

        media = MediaFileUpload(self.file_path, mimetype=mime_type)

        # Upload the file
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        out = 'Upload Successful....... \n File {} uploaded to folder {} in google drive'.format(file_name,self.file_in_folder)
        return (out,'File ID: %s' % file.get('id'))


    def _create_folder(self, drive_service):
        gdrive_folder_name = self.file_in_folder
        # Check if the folder already exists
        query = f"name='{gdrive_folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query).execute().get('files', [])
        if results:
            return results[0]['id']
        else:

            folder_metadata = {
                'name': gdrive_folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')


if __name__ == '__main__':
    file_to_upload = 'D:/github/FILE_TO_UPLOAD.mov'
    token = 'D:/github/__Secrets/token.json'
    client_secret = 'D:/github/__Secrets/mar_credentials.json'
    folder_name = 'Week_03_Python_test'
    file_up=GDriveUtils(client_secret,token,file_to_upload, folder_name)
    file_up.upload_file(local_path=True)