import time
import geopy
import pandas as pd
import math

from consts import Consts


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


def parse_csv(path_csv, address_col = 'Address'):
    #must have Address column
    #should have: Category, ID, Other_Information, Status

    df = pd.read_csv(path_csv, index_col=0)

    if not (Consts.lat_col in list(df)) and not(Consts.long_col in list(df)):
        df[Consts.lat_col] = math.nan
        df[Consts.long_col] = math.nan
    empty_rows = df[address_col].isnull()
    for i, row in df.iterrows():
        if empty_rows[i]:
            continue
        if math.isnan(row[Consts.lat_col]) or math.isnan(row[Consts.long_col]):
            address = row[address_col]
            gps_location = get_location_from_address(address)
            if gps_location is None:
                print(f'address was not found for {address}')
            else:
                df.at[i, Consts.lat_col] = gps_location.latitude
                df.at[i, Consts.long_col] = gps_location.longitude
                df.at[i, Consts.address_found_col] = gps_location.address

    df.to_csv('reports_updated.csv')

    print('done!!')

