import time
import geopy
import pandas as pd

def get_location_from_address(address):
    gpsLocation = None
    locationToLook = address.replace(',', '')

    time.sleep(1)
    get = False
    try:
        # get new in here:
        # https://console.developers.google.com/
        backUpGeolocator = geopy.geocoders.GoogleV3('AIzaSyDujiJfrz1GorKb6p-HrzCE-oL_A8GN058')
        gpsLocation = backUpGeolocator.geocode(locationToLook)
        get = True
    except Exception as e:
        print(e)

    if not get:
        try:
            backUpGeolocator = geopy.geocoders.Bing(
                'Aj4HplPNElwLP_temgYW0JCF_3Jh0oMYCIUH4yxLK32PwAwP9G2bmTABcMpLwciY')
            gpsLocation = backUpGeolocator.geocode(locationToLook)
        except Exception as e:
            print(e)

    return gpsLocation

def parse_csv(path_csv):
    #must have Address column
    #should have: Category, ID, Other_Information, Status

    df = pd.read_csv(path_csv, index_col=0)
    addresses = df['Address'].to_numpy()
    gps_locatoins = [get_location_from_address(address) for address in addresses]
    addresses_found = [x.address for x in gps_locatoins]
    lats = [x.latitude for x in gps_locatoins]
    longs = [x.longitude for x in gps_locatoins]
    df['addresses_found']=addresses_found
    df['lat']=lats
    df['long']=longs

    df.to_csv('reports_updated.csv')

    print('done!!')

