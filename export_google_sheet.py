# encoding: utf-8

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt

NAME_INDEX = 1
CYCLE_INDEX = 2
QUADRANT_INDEX = 3
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
            wks.append_row([blip.name, blip.cycle, blip.quadrant, blip.is_new, "Suggested by: " + blip.user])
        else:
            insert_row = True
            for cell in cells:
                # Check first if they are in the same quadrant and cycle
                quadrant = wks.cell(cell.row, QUADRANT_INDEX).value
                cycle = wks.cell(cell.row, CYCLE_INDEX).value
                desc = wks.cell(cell.row, DESCRIPTION_INDEX).value
                if quadrant == blip.quadrant and cycle == blip.cycle:
                    wks.update_cell(cell.row, DESCRIPTION_INDEX, desc + ", " + blip.user)
                    insert_row = False
                    break
            if insert_row:
                wks.append_row([blip.name, blip.cycle, blip.quadrant, blip.is_new, "Suggested by: " + blip.user])

def export_all(tweets):
    scope = ['https://spreadsheets.google.com/feeds']
    
    sheet_name = os.getenv('GSPREAD_SHEET_NAME')
    worksheet_previous_radar_name = os.getenv('GSPREAD_PREVIOUS_RADAR_NAME')

    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GSPREAD_JSON_FILE'), scope)
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
