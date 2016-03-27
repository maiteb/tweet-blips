# encoding: utf-8

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt

NAME_INDEX = 1
QUADRANT_INDEX = 2
CYCLE_INDEX = 3
DESCRIPTION_INDEX = 5

class Blip:
    def __init__(self, tweet, is_new):
        self.quadrant = tweet.quadrant
        self.cycle = tweet.cycle
        self.name = tweet.blip.capitalize()
        self.user = tweet.name + " (@" + tweet.username + ")"
        self.is_new = is_new

def _check_if_is_new(blip_name, previous_blips):
    if blip_name in previous_blips:
        return False
    else:
        return True

def _export_to_google(wks, blips_to_export):
    for blip in blips_to_export:
        # First we will check if the blip is already present
        cells = wks.findall(blip.name)
        if not cells:
            wks.append_row([blip.name, blip.quadrant, blip.cycle, blip.is_new, "Suggested by: " + blip.user])
        else:
            print cells
            insert_row = True
            for cell in cells:
                # Check first if they are in the same quadrant and cycle
                quadrant = wks.cell(cell.row, QUADRANT_INDEX)
                cycle = wks.cell(cell.row, CYCLE_INDEX)
                desc = wks.cell(cell.row, DESCRIPTION_INDEX)
                if quadrant == blip.quadrant and cycle == blip.cycle:
                    wks.update_cell(cell.row, DESCRIPTION_INDEX, desc + ", " + blip.user)
                    insert_row = False
                    break
            if insert_row:
                wks.append_row([blip.name, blip.quadrant, blip.cycle, blip.is_new, "Suggested by: " + blip.user])

def export_all(tweets):
    scope = ['https://spreadsheets.google.com/feeds']
    client_email = os.getenv('GSPREAD_CLIENT_EMAIL')
    private_key = os.getenv('GSPREAD_PRIVATE_KEY').encode()
    private_key_id = os.getenv('GSPREAD_PRIVATE_KEY_ID')
    signer = crypt.Signer.from_string(private_key)
    sheet_name = os.getenv('GSPREAD_SHEET_NAME')
    worksheet_previous_radar_name = os.getenv('GSPREAD_PREVIOUS_RADAR_NAME')

    credentials = ServiceAccountCredentials(service_account_email=client_email, signer=signer, private_key_id=private_key_id, scopes=scope)
    gc = gspread.authorize(credentials)

    sht = gc.open(sheet_name)
    wks_previous_radar = sht.worksheet(worksheet_previous_radar_name)
    previous_blips = wks_previous_radar.col_values(1)
    # we need to remove the first item because it is a label one
    previous_blips.pop(0)

    previous_blips = [text.lower() for text in previous_blips]
    wks_new_radar = sht.sheet1

    blips_to_export = []
    for tweet in tweets:
        blips_to_export.append(Blip(tweet, _check_if_is_new(tweet.blip, previous_blips)))

    _export_to_google(wks_new_radar, blips_to_export)
