# encoding: utf-8

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt

scope = ['https://spreadsheets.google.com/feeds']
client_email = os.getenv('GSPREAD_CLIENT_EMAIL')
private_key = os.getenv('GSPREAD_PRIVATE_KEY').encode()
private_key_id = os.getenv('GSPREAD_PRIVATE_KEY_ID')
signer = crypt.Signer.from_string(private_key)
sheet_name = os.getenv('GSPREAD_SHEET_NAME')

credentials = ServiceAccountCredentials(service_account_email=client_email, signer=signer, private_key_id=private_key_id, scopes=scope)
gc = gspread.authorize(credentials)

wks = gc.open(sheet_name).sheet1

print wks.acell('A1')
