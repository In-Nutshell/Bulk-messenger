# Telegram Bulk Messenger

A powerful bulk messaging tool using [Telethon](https://github.com/LonamiWebs/Telethon) for sending Telegram messages to multiple users with intelligent fallback and persistent JSON-based contact management.

---

## 🚀 Features

- ✅ Automatically stores contact info and prefers `user_id` in future sends
- 📁 JSON database (`contacts_database.json`) to track and enrich contacts
- 📊 CSV + JSON reports of message results
- 🛡️ Anti-spam protection: safe delays and flood wait handling
- 🔄 Retry mechanism and identifier fallback: `user_id` → `username` → `phone`
- 📂 Loads contacts from `contacts.csv` file

---

## 📁 Project Structure

├── config/ # App config (paths, API keys)
│ └── config.py
│
├── data/ # Runtime data (ignored in Git)
│ ├── contacts.csv
│ ├── contacts_database.json
│ └── messaging_report.json
│
├── logs/ # Logging output
│ └── telegram_messenger.log
│
├── sessions/ # Telethon session files (auto-created)
│
├── src/ # Main app logic (modularized)
│ ├── core/ # Telegram client, database handling
│ │ ├── telegram_client.py
│ │ └── database.py
│ │
│ ├── messaging/ # Messaging logic
│ │ └── message_sender.py
│ │
│ ├── reporting/ # Report generation
│ │ └── reporter.py
│ │
│ └── utils/ # Logging, safety rules, UI
│ ├── logger.py
│ ├── safety_manager.py
│ └── ui.py
│
├── .env # API keys (never committed)
├── .gitignore # Git exclusions
├── main.py # Entry point
└── README.md # This file

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install telethon python-dotenv

### 2. Create .env File

API_ID=your_api_id_here
API_HASH=your_api_hash_her
Do NOT commit .env. Your credentials should stay local.

### 3. Run the Project
python main.py



🔒 Anti-Spam Features
| Feature               | Description                               |
| --------------------- | ----------------------------------------- |
| ✅ Delay               | Default: 5 seconds between messages       |
| ✅ Daily Limit         | Max 50 messages/day (adjustable)          |
| ✅ Retry Strategy      | Handles rate limits, user privacy         |
| ✅ Identifier Fallback | Tries user\_id, then username, then phone |

```
