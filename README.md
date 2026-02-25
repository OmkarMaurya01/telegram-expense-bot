# Tracking Expenses Bot

A Telegram bot to track expenses directly into Google Sheets.


## System Architecture
┌────────────┐
│   User     │
│ Telegram   │
└─────┬──────┘
      │
      ▼
┌──────────────────┐
│ Telegram Bot     │
│ (Polling/Webhook)│
└─────┬────────────┘
      │
      ▼
┌────────────────────┐
│ Command Dispatcher │
│ (Message Router)   │
└─────┬──────────────┘
      │
      ├───────────────┐
      ▼               ▼
┌──────────────┐  ┌───────────────────┐
│ Sheet Manager│  │ Expense Handler   │
│ (System Cmds)│  │ (Insert Only)     │
└─────┬────────┘  └─────────┬─────────┘
      │                     │
      ▼                     ▼
┌──────────────┐       ┌──────────────┐
│ Google Drive │       │ Google Sheets│
│ API          │       │ API          │
└──────────────┘       └──────────────┘
      │
      ▼
┌────────────────────┐
│ Local Notebook     │
│ (JSON State Files) │
└────────────────────┘


## Project Structure

```
tracking-expenses/
├── src/
│   ├── main.py                     # entry point
│   ├── bot/telegram_bot.py         # Telegram polling/webhook only
│   ├── dispatcher/router.py        # route messages to handlers
│   ├── handlers/
│   │   ├── sheet_manager.py        # system commands (ls, mk, select, del)
│   │   └── expense_handler.py      # parse expense & orchestrate insert
│   ├── api/
│   │   ├── drive_api.py            # Google Drive API (create/delete sheets)
│   │   └── sheets_api.py           # Google Sheets API (append rows)
│   ├── state/
│   │   ├── sheets.json             # bot-managed sheets registry
│   │   └── active_sheet.json       # currently selected sheet
│   └── utils/
│       ├── config.py               # env vars, constants
│       └── logger.py               # centralized logging
├── credentials/
│   └── service_account.json        # Google Service Account credentials
├── logs/
│   └── app.log                     # Application logs
├── tests/                          # Test suite
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```




## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your `service_account.json` in the `credentials/` directory.

3. Create a `.env` file with your `TELEGRAM_TOKEN`.

4. Run the bot:
   ```bash
   python src/main.py
   ```
