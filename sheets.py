# sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDENTIALS_FILE

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(credentials)

def get_managers():
    sheet = client.open_by_url(MANAGERS_SHEET_URL).sheet1
    return [row[0] for row in sheet.get_all_values()[1:] if row[0]]

def get_products_by_brand_and_category(brand, category):
    sheet = client.open_by_url(PRODUCTS_SHEET_URL).sheet1
    rows = sheet.get_all_values()[1:]
    return [row[2] for row in rows if row[0] == brand and row[1] == category]

def get_all_brands():
    sheet = client.open_by_url(PRODUCTS_SHEET_URL).sheet1
    rows = sheet.get_all_values()[1:]
    return sorted(set(row[0] for row in rows if row[0]))

def get_categories_by_brand(brand):
    sheet = client.open_by_url(PRODUCTS_SHEET_URL).sheet1
    rows = sheet.get_all_values()[1:]
    return sorted(set(row[1] for row in rows if row[0] == brand))

def save_order(manager, brand, category, product, quantity, date, comment):
    sheet = client.open_by_url(ORDERS_SHEET_URL).sheet1
    sheet.append_row([manager, brand, category, product, quantity, date, comment])
