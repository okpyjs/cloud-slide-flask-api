import io
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class Drive:
    def __init__(self) -> None:
        # setting drive
        self.scopes = ["https://www.googleapis.com/auth/drive"]
        SERVICE_ACCOUNT_FILE = "masayuki_service.json"
        self.creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=self.scopes
        )
        self.service = build("drive", "v3", credentials=self.creds)

    def get_file_ids(self, folder_id):
        results = []
        page_token = None

        while True:
            response = (
                self.service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )

            files = response.get("files", [])
            results.extend(files)

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return results

    def merge(self, slides):
        print(slides)

    def download(self, id: str):
        # Create a BytesIO object to store the downloaded file
        file_stream = io.BytesIO()

        # Download the file
        request = self.service.files().get_media(fileId=id)
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

        # Save the downloaded file
        file_stream.seek(0)
        with open(f"{id}.pptx", "wb") as f:
            f.write(file_stream.read())

    def upload(self, file_path):
        # Create a file metadata
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [os.environ.get("SAVE_FOLDER_ID")],
        }

        media = MediaFileUpload(file_path)

        # Upload the file
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id, name")
            .execute()
        )

        # Print the ID of the uploaded file
        print("File ID: ", file["id"])

        file_id = file["id"]
        file_name = file["name"]

        return {"id": file_id, "name": file_name}
