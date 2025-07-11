import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Google Sheets credentials.json ni to'g'ridan-to'g'ri string ko'rinishida env dan o'qib olish
import json
import tempfile

credentials_str = os.getenv("SHEET_CREDENTIALS_JSON")
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
    temp_file.write(credentials_str.encode())
    GOOGLE_CREDENTIALS_PATH = temp_file.name
