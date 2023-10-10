import time
import geopy
import pandas as pd
import math
import random
import sys
try:
    import httpx
except:
    import requests
from pyproj import Transformer

from consts import Consts


transformer = Transformer.from_crs("EPSG:6991", "EPSG:4326")


def randomize_coordinates(args,location):
    new_location = location
    if args.random_same_location:
        rand_num = 1 if random.random() < 0.5 else -1
        rand_num = rand_num * random.uniform(0.1, 0.2)/500
        new_location = location + rand_num
    return new_location

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
        if not gpsLocation:
            gpsLocation = get_location_using_govmap(locationToLook)

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

def get_location_using_govmap(locationToLook):
    gpsLocation = None
    try:
        url = f'https://es.govmap.gov.il/TldSearch/api/DetailsByQuery?query={locationToLook}&lyrs=-1&gid=govmap'
        if 'httpx' in sys.modules:
            govmap_response = httpx.get(url)
        else:
            govmap_response = requests.get(url)
        if govmap_response.status_code != 200:
            return None

        data = govmap_response.json()

        if not data['data']:
            return None
        if data['data'].get('ADDRESS'):
            found = data['data']['ADDRESS'][0]
        elif data['data'].get('SETTLEMENT'):
            found = data['data']['SETTLEMENT'][0]
        else:
            return None
        gpsLocation =  geopy.location.Location(found['ResultLable'],
                                       transformer.transform(found['X'], found['Y']), True)
    except Exception as e:
        print(f'could not find address for {locationToLook}')

    return gpsLocation

def parse_csv(path_csv, args = None ):
    #must have Address column
    #should have: Category, ID, Other_Information, Status

    df = pd.read_csv(path_csv)
    headers = list(df)
    if (len(set(headers)) != len(headers)):
        print('Warning: There are multiple columns with the same name. It might cause issues')
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
                df.at[i, Consts.lat_col] = randomize_coordinates(args,Consts.default_lat)
                df.at[i, Consts.long_col] = randomize_coordinates(args,Consts.default_long)

            else:
                df.at[i, Consts.lat_col] = randomize_coordinates(args,gps_location.latitude)
                df.at[i, Consts.long_col] = randomize_coordinates(args,gps_location.longitude)
                df.at[i, Consts.address_found_col] = gps_location.address

    df.to_csv('reports_updated.csv', index=False)

    print('done!!')
