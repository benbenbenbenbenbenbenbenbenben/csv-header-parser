from csv_header import CSVParser, get_rows_for_indexes, get_x_rows_for_index
 
csv_file_path = "data_house.csv"  # Replace with the path to your CSV file

if __name__ == "__main__":
    # Define headers with aliases
    headers = {
        'required': {
            'Address': ['property address', 'location', 'house address'],
            'Price': ['listing price', 'cost', 'sale price'],
            'Bedrooms': ['number of bedrooms', 'beds'],
            'Bathrooms': ['number of bathrooms', 'baths'],
        },
        'optional': {
            'Square Footage': ['area', 'size', 'sqft'],
            'Year Built': ['construction year', 'built year'],
            'Lot Size': ['land size', 'plot size'],
            'Garage': ['carport', 'parking'],
            'Amenities': ['features', 'extras'],
            'Notes': ['description', 'additional info'],
        }
    }

    max_rows = 5

    parser = CSVParser(headers, max_rows)

    result, df = parser.parse_csv(csv_file_path)

    if "error" not in result:
        # Load the DataFrame with the correct headers
        header_start_row = result['header_start_row']
        header_indices = result['header_indices']

        # Request `x` rows for a single index
        address_index = header_indices.get('Address', None)
        try:
            first_three_addresses = get_x_rows_for_index(df, address_index, header_start_row, x=3)
            print("\nFirst three addresses:")
            print(first_three_addresses)
        except ValueError as e:
            print(e)

        # Request `x` rows for multiple indexes
        requested_indexes = [
            header_indices.get('Address', None),
            header_indices.get('Price', None),
            header_indices.get('Bedrooms', None),
        ]
        try:
            rows_for_columns = get_rows_for_indexes(df, requested_indexes, header_start_row, rows=3)
            print("\nRows for requested columns:")
            for index, rows in rows_for_columns.items():
                print(f"Column {index}:\n{rows}\n")
        except ValueError as e:
            print(e)
    else:
        print(result["error"])
