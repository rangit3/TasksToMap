import time
import geopy
import pandas as pd
import math

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


def parse_csv(path_csv):
    #must have Address column
    #should have: Category, ID, Other_Information, Status

    df = pd.read_csv(path_csv, index_col=0)
    if not ('lat' in list(df)) and not('long' in list(df)):
        df["lat"] = math.nan
        df["long"] = math.nan
    empty_rows = df['Address'].isnull()
    for i, row in df.iterrows():
        if empty_rows[i]:
            continue
        if math.isnan(row["lat"]) or math.isnan(row["long"]):
            address = row["Address"]
            gps_location = get_location_from_address(address)
            if gps_location is None:
                print(f'address was not found for {address}')
            else:
                df.at[i,"lat"] = gps_location.latitude
                df.at[i,"long"] = gps_location.longitude
                df.at[i,"address_found"] = gps_location.address

    df.to_csv('reports_updated.csv')

    print('done!!')

