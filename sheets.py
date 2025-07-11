import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)

# Buyurtmalar jadvali (3-link)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1I2mgQHFqdFcRnVt0D4WczGKOztn-7XPauB7NR33fX0I").sheet1

def add_order(data: list):
    sheet.append_row(data)
