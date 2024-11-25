# CSV Parser for Headers

Python tool for parsing CSV files to detect and validate headers and data row based on required and optional columns. Handles if headers were merged spanned different rows before data starts.

## Features
- Detects and validates headers 
- Finds data row start
- Supports both required and optional fields

## Example Headers Configuration
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
