from parse_csv import parse_csv


def main():
    path_csv = 'reports.csv'
    address_col = 'Address'
    parse_csv(path_csv, address_col = address_col)

if __name__ == '__main__':
    main()
