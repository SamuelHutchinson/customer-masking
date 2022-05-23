import sys
from column import ColumnFactory, ColumnInterface
from serialisers import SerialiseCustomer
import serialisers

def get_customers(input_file):
    """Takes in an input file and returns a masked dataset"""

    # Read in the CSV File
    lines = []
    with open(input_file, "r") as file:
        for line in file:
            if not line.isspace():
                lines.append(line.strip())
    # Extract columns from CSV file into a dictionary
    customer_data = get_customer_columns(lines[1:]) # Top row contains headings in CSV, so want second row downwards for data
    # Columns to be masked
    customer_data["Name"] = transform_customer_data(customer_data["Name"], "Alphanumeric")
    customer_data["Email"] = transform_customer_data(customer_data["Email"], "Alphanumeric")
    customer_data["Billing"] = transform_customer_data(customer_data["Billing"], "Numeric")

    
    # Symbols to be excluded when masking.
    # Included a ' ' at the end to mask only letter appearances on alphanumeric columns
    rules = ['@','.',',',' '] 
    mask = 'X'
    mask_data(customer_data, rules, mask)
    return customer_data

def get_customer_columns(table):
    """Extracts columns from the dataset into a dictionary"""

    result = {
        "ID": [],
        "Name": [],
        "Email": [],
        "Billing": [],
        "Location": [],
    }
    for line in table: # Each row in the provided table
        record = line.split(',')
        result["ID"].append(record[0])
        result["Name"].append(record[1])
        result["Email"].append(record[2])
        result["Billing"].append(record[3])
        result["Location"].append(record[4])

    return result

def transform_customer_data(column, column_type):
    """Provides a column object to perform masking operations on"""

    customer = ColumnFactory()
    column = customer.return_object(column_type, column)
    return column

def mask_data(record, rules, mask):
    """Masks columns in a dataset given a mask and rules"""

    for heading, data in record.items():
        if isinstance(data, ColumnInterface): # Focus only on columns identified for masking by the user.
            data.mask(mask=mask, rules=rules)

def output(table, output=None):
    """Serialises the data back into a format specified by the user e.g. CSV or standard output"""

    serialise_customer = SerialiseCustomer()
    csv = serialise_customer.get_serialiser("CSV", data=table, output_file=output)
    csv.serialise()
    stdout = serialise_customer.get_serialiser("STDOUT", data=table)
    stdout.serialise("Name", "Billing") # Column values to be printed to stdout

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if input_file.lower().endswith(('csv')): # If file format is of csv
        customer_data = get_customers(input_file)
        output(customer_data, output_file)
    else:
        raise ValueError(f"Invalid file input: {input_file}. Input file needs to be of CSV format")