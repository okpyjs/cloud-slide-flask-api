import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


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
                    fields="nextPageToken, files(id)",
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
