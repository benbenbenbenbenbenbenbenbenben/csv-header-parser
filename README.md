# csv-header-parser
Python tool for parsing CSV files to detect and validate headers and data row based on required and optional columns. Handles if headers were merged spanned different rows before data starts.

# CSV Parser for House Listings

A Python tool to parse and validate CSV files for house listings, ensuring key features like address, price, and number of rooms are correctly identified.

## Features
- Detects and validates headers for house attributes such as address, price, and amenities.
- Supports both required and optional fields, allowing for flexible data processing.

## Headers Configuration
```python
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
