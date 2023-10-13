from parse_google_sheets import parse_google_sheet
from parse_csv import parse_csv
import argparse

def main():
    arg_parser  = argparse.ArgumentParser()
    arg_parser .add_argument("--index", default=-1, type= int,
                           help="index of column that contain the address")
    arg_parser .add_argument("--address_col", default=None,
                           help="name of column that contain the address")
    arg_parser.add_argument("--random_same_location", default=True,
                            help="If city is provided, it will change a little the pin location for different tasks")
    arg_parser.add_argument("--ignore_pairs", default=None,
                            help="Pairs of column name and value to filter out separated by '=',"
                                 "each pair separated by a semicolon")
    arg_parser.add_argument("--fill_pairs", default=None,
                            help="Pairs of column name and default value to fill empty cells separated by '=',"
                                 "each pair separated by a semicolon")

    args = arg_parser.parse_args()

    path_csv = 'reports.csv'
    parse_csv(path_csv, args = args)
    # parse_google_sheet(args = args)

if __name__ == '__main__':
    main()
