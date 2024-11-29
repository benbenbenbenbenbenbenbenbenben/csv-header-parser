import pandas as pd

class CSVParser:
    """
    A class to parse and process CSV files for specific headers and data rows.

    Attributes:
        headers (dict): A dictionary with required and optional headers as keys and their aliases as values.
    """

    def __init__(self, headers, max_rows=5):
        """
        Initializes the CSVParser.

        Args:
            headers (dict): Dictionary with two keys: 'required' and 'optional'.
                Each key's value should be a dict where header names map to their list of aliases.
                Example:
                    {
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
        """
        self.required_headers = headers.get('required', {})
        self.optional_headers = headers.get('optional', {})
        self.max_rows = max_rows

    def find_header_row(self, dataframe):
        """
        Finds the header rows and assigns column indices for required and optional headers.

        Args:
            dataframe (pd.DataFrame): The dataframe to search.

        Returns:
            tuple: (header_start_row, header_indices, missing_required_headers, optional_header_indices)
        """
        collected_headers = {}
        missing_required_headers = list(self.required_headers.keys())
        last_match_row = None  # Track the last matched row for required or optional headers

        for i, row in dataframe.head(self.max_rows).iterrows():
            header_row = [
                str(col).strip().lower().replace('\n', ' ') if pd.notna(col) else None
                for col in row.values.tolist()
            ]

            # Match required headers
            for header, aliases in self.required_headers.items():
                normalized_header = header.strip().lower()
                if normalized_header in header_row and header not in collected_headers:
                    collected_headers[header] = header_row.index(normalized_header)
                    if header in missing_required_headers:
                        missing_required_headers.remove(header)
                    last_match_row = i
                elif any(alias.lower() in header_row for alias in aliases):
                    alias_match = next(alias.lower() for alias in aliases if alias.lower() in header_row)
                    collected_headers[header] = header_row.index(alias_match)
                    if header in missing_required_headers:
                        missing_required_headers.remove(header)
                    last_match_row = i

            # Match optional headers
            for header, aliases in self.optional_headers.items():
                normalized_header = header.strip().lower()
                if normalized_header in header_row and header not in collected_headers:
                    collected_headers[header] = header_row.index(normalized_header)
                    last_match_row = i
                elif any(alias.lower() in header_row for alias in aliases):
                    alias_match = next(alias.lower() for alias in aliases if alias.lower() in header_row)
                    collected_headers[header] = header_row.index(alias_match)
                    last_match_row = i

            # # Stop early if all required headers are found
            # if not missing_required_headers:
            #     break

        # Determine header start row
        header_start_row = last_match_row + 1 if last_match_row is not None else None

        # If no required headers were found, return an error
        if not collected_headers.keys() & self.required_headers.keys():
            return None, {}, missing_required_headers, {}

        required_indices = {key: collected_headers[key] for key in self.required_headers if key in collected_headers}
        optional_indices = {key: collected_headers[key] for key in self.optional_headers if key in collected_headers}

        return header_start_row, required_indices, missing_required_headers, optional_indices

    def parse_csv(self, csv_file_path):
        """
        Parses a CSV file to find headers and data start row.

        Args:
            csv_file_path (str): Path to the CSV file.

        Returns:
            dict: Parsed results or error information.
        """
        try:
            df = pd.read_csv(csv_file_path, header=None)
            header_start_row, header_indices, missing_headers, optional_indices = self.find_header_row(df)

            if len(missing_headers) > 0:
                return {"error": f"Required headers not found: {', '.join(missing_headers)}"}

            return {
                "header_start_row": header_start_row,
                "header_indices": header_indices,
                "optional_indices": optional_indices,     
            }, df
        except Exception as e:
            return {"error": f"An error occurred: {e}"}



def get_x_rows_for_index(df, column_index, header_start_row, x=3):
    """
    Retrieves `x` rows starting from the given header start row for the specified column index.

    Args:
        df (pd.DataFrame): The DataFrame to retrieve rows from.
        column_index (int): The index of the column.
        header_start_row (int): The starting row for data.
        x (int): The number of rows to retrieve.

    Returns:
        pd.Series: A Series containing the requested rows.
    """
    if column_index is None or column_index >= len(df.columns):
        raise ValueError("Invalid column index provided.")
    return df.iloc[header_start_row:header_start_row + x, column_index]

def get_rows_for_indexes(df, column_indexes, header_start_row, rows=3):
    """
    Retrieves rows starting from the given header start row for each column specified by the indexes.

    Args:
        df (pd.DataFrame): The DataFrame to retrieve rows from.
        column_indexes (list): List of column indexes to fetch data from.
        header_start_row (int): The starting row for data.
        rows (int): The number of rows to retrieve.

    Returns:
        dict: A dictionary where keys are column indexes and values are Series of requested rows.
    """
    if not column_indexes:
        raise ValueError("No column indexes provided.")
    
    results = {}
    for index in column_indexes:
        if index is None or index >= len(df.columns):
            results[index] = f"Invalid column index: {index}"
        else:
            results[index] = df.iloc[header_start_row:header_start_row + rows, index]
    return results

def forward_fill_column(df, col_index):
    """
    Forward-fills cells in a specified column index to handle merged or missing values.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        col_index (int): The index of the column to forward-fill.

    Returns:
        pd.DataFrame: The modified DataFrame with forward-filled values in the specified column.
    """
    if col_index is not None and col_index < len(df.columns):
        df.iloc[:, col_index] = df.iloc[:, col_index].ffill()
        print(f"Forward-filled column at index: {col_index}")
    else:
        print(f"Column index {col_index} is invalid or not found.")
    return df
