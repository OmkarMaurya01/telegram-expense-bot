import gspread
import logging
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)


class SheetsAPI:
    """
    Thin wrapper over Google Sheets API (via gspread).
    Responsible ONLY for appending rows.
    """

    def __init__(
        self,
        credentials_path: str = "credentials/service_account.json",
        sheet_id: str | None = None,
        worksheet_index: int = 0,
    ):
        """
        :param credentials_path: path to service account json
        :param sheet_id: Google Sheet ID (required)
        :param worksheet_index: which tab to use (default first tab)
        """

        if not sheet_id:
            raise ValueError("sheet_id is required for SheetsAPI")

        self.sheet_id = sheet_id
        self.worksheet_index = worksheet_index

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]

        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes,
        )

        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(sheet_id)
        self.worksheet = self.sheet.get_worksheet(worksheet_index)

        logger.info("[SheetsAPI] Connected to Google Sheet")

    # ---------------------------------
    # Public API
    # ---------------------------------

    def append_row(self, row: list) -> None:
        """
        Append a single row to the sheet.
        """

        if not isinstance(row, list):
            raise ValueError("Row must be a list")

        logger.info(f"[SheetsAPI] Appending row: {row}")

        try:
            self.worksheet.append_row(
                row,
                value_input_option="USER_ENTERED"
            )
        except Exception:
            logger.exception("[SheetsAPI] Failed to append row")
            raise
