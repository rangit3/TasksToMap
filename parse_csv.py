import time
import geopy
import pandas as pd
import math

from consts import Consts

def get_address_col(headers, args = None):
    if args is not None:
        if args.address_col is not None:
            address_col_name = args.address_col
            address_col_name_index = headers.index(address_col_name)
        elif args.index > -1:
            address_col_name = headers[args.index]
            address_col_name_index = args.index
        else:
            address_col_name = Consts.address_col
            address_col_name_index = headers.index(address_col_name)
    else:
        address_col_name = Consts.address_col
        address_col_name_index = headers.index(address_col_name)
    print(f'Address column: {address_col_name}')
    return address_col_name, address_col_name_index

def get_location_from_address(address):
    locationToLook = address.replace(',', '')

    time.sleep(1)
    gpsLocation = None
    get = False

    # get, gpsLocation = get_location_using_google(locationToLook)
    if not get:
        gpsLocation = get_location_using_bing(locationToLook)

    return gpsLocation


def get_location_using_bing(locationToLook):
    gpsLocation = None
    try:
        backUpGeolocator = geopy.geocoders.Bing(
            'Aj4HplPNElwLP_temgYW0JCF_3Jh0oMYCIUH4yxLK32PwAwP9G2bmTABcMpLwciY')
        gpsLocation = backUpGeolocator.geocode(locationToLook)
    except Exception as e:
        print(e)
    return gpsLocation


def get_location_using_google(locationToLook):
    get = False
    gpsLocation = None
    try:
        # get new in here:
        # https://console.developers.google.com/
        backUpGeolocator = geopy.geocoders.GoogleV3('')
        gpsLocation = backUpGeolocator.geocode(locationToLook)
        get = True
    except Exception as e:
        print(e)
    return get, gpsLocation


def parse_csv(path_csv, args = None ):
    #must have Address column
    #should have: Category, ID, Other_Information, Status

    df = pd.read_csv(path_csv)
    headers = list(df)
    address_col_name, address_col_name_index = get_address_col(headers, args = args)

    if not (Consts.lat_col in headers) and not(Consts.long_col in headers):
        df[Consts.lat_col] = math.nan
        df[Consts.long_col] = math.nan
    empty_rows = df[address_col_name].isnull()
    for i, row in df.iterrows():
        if empty_rows[i]:
            continue
        if math.isnan(row[Consts.lat_col]) or math.isnan(row[Consts.long_col]):
            address = row[address_col_name]
            gps_location = get_location_from_address(address)
            if gps_location is None:
                print(f'address was not found for {address}')
            else:
                df.at[i, Consts.lat_col] = gps_location.latitude
                df.at[i, Consts.long_col] = gps_location.longitude
                df.at[i, Consts.address_found_col] = gps_location.address

    df.to_csv('reports_updated.csv', index=False)

    print('done!!')

