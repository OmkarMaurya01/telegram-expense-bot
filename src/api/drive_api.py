
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class DriveAPI:
    """
    Thin wrapper around Google Drive API.
    Handles spreadsheet-level operations only.
    """

    def __init__(
        self,
        credentials_path: str = "credentials/service_account.json",
    ):
        self.credentials_path = credentials_path
        self.service = self._build_service()

    def _build_service(self):
        """
        Authenticate and build Drive API service.
        """
        scopes = ["https://www.googleapis.com/auth/drive"]

        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=scopes,
        )

        service = build("drive", "v3", credentials=creds)
        logger.info("[DriveAPI] Google Drive service initialized")

        return service

    # ---------------------------------
    # Public API methods
    # ---------------------------------

    def create_spreadsheet(self, name: str) -> dict:
        """
        Create a new Google Spreadsheet.

        Returns:
            {
                "sheet_id": str,
                "sheet_name": str
            }
        """
        logger.info(f"[DriveAPI] Creating spreadsheet: {name}")

        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }

        file = (
            self.service.files()
            .create(
                body=file_metadata,
                fields="id, name",
            )
            .execute()
        )

        logger.info(
            f"[DriveAPI] Spreadsheet created | ID: {file['id']} | Name: {file['name']}"
        )

        return {
            "sheet_id": file["id"],
            "sheet_name": file["name"],
        }

    def delete_spreadsheet(self, sheet_id: str) -> bool:
        """
        Delete a Google Spreadsheet by ID.
        """
        logger.info(f"[DriveAPI] Deleting spreadsheet: {sheet_id}")

        try:
            self.service.files().delete(fileId=sheet_id).execute()
            logger.info(f"[DriveAPI] Spreadsheet deleted: {sheet_id}")
            return True
        except Exception:
            logger.exception("[DriveAPI] Failed to delete spreadsheet")
            return False

    def list_spreadsheets(self) -> list:
        """
        List spreadsheets accessible to the service account.

        Returns:
            [
                {"sheet_id": str, "sheet_name": str}
            ]
        """
        logger.info("[DriveAPI] Listing spreadsheets")

        results = (
            self.service.files()
            .list(
                q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
                fields="files(id, name)",
            )
            .execute()
        )

        files = results.get("files", [])

        sheets = [
            {
                "sheet_id": f["id"],
                "sheet_name": f["name"],
            }
            for f in files
        ]

        logger.info(f"[DriveAPI] Found {len(sheets)} spreadsheets")

        return sheets


obj = DriveAPI()
obj.create_spreadsheet("Test")