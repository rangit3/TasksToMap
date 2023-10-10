from collections import namedtuple
from typing import List

EmptyValueReplacer = namedtuple("EmptyValueReplacer", ["col_name", "replacer"])
ValueToIgnore = namedtuple("ValueToIgnore", ["col_name", "val_to_ignore"])

class Consts(object):
    lat_col = "lat"
    long_col = "long"
    address_found_col = "address_found"
    default_lat = 34.74852501 #Cyprus
    default_long =32.99089267
    empty_vals_replacers: List[EmptyValueReplacer] = []
    ignore_values: List[ValueToIgnore] = []

    address_col = 'Address'
