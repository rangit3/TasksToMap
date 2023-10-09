from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import parse_csv
from consts import Consts

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1XdHPZfxvCXPfMgnPLUfjwQaibv6KuguEUbNslr8W7vU'
SAMPLE_RANGE_NAME = 'A1:1'


def get_column_length(sheet) -> int:
    """
    Finds the last column in use
    Args:
        sheet: the sheet where the data is

    Returns:
        the index, -1 if no data is found
    """
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return -1

    return len(values[0])


def parse_sheet(sheet, args = None):
    column_length = get_column_length(sheet)
    last_column = chr(ord('A') + column_length)
    print(last_column)
    range = f'A1:' + last_column
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    headers = values[0]
    address_col, address_column_index = parse_csv.get_address_col(headers, args)
    new_data = [[Consts.address_found_col, Consts.lat_col, Consts.long_col ]]
    update_range = chr(ord('A') + column_length + 1) + '1'
    for idx, row in enumerate(values[1:]):
        address = parse_csv.get_location_from_address(row[address_column_index])
        new_data.append([address.address, address.latitude, address.longitude])

    print(sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=update_range,
                                valueInputOption='USER_ENTERED',
                                body={'values': new_data}).execute())


def parse_google_sheet(path_csv = None, args = None):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        parse_sheet(sheet)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    parse_google_sheet()
