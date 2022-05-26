import sys
from column import ColumnFactory, ColumnInterface
from outputs import Outputs
from inputs import Inputs
import time

def get_customers(input_file):
    """Takes in an input file and returns a masked dataset"""
    inputs = Inputs()
    csv_input = inputs.get_input("CSV", input_file)
    csv_input.get()
    # Columns to be masked
    csv_input.data["Name"] = get_column(csv_input.data["Name"], "Alphanumeric")
    csv_input.data["Email"] = get_column(csv_input.data["Email"], "Alphanumeric")
    csv_input.data["Billing"] = get_column(csv_input.data["Billing"], "Numeric")

    # Symbols to be excluded when masking.
    # Included a ' ' at the end to mask only letter appearances on alphanumeric columns
    rules = ['@','.',',',' ']
    mask = 'X'
    mask_data(csv_input.data, rules, mask)
    return csv_input

def csv_reader(input_file):
    for line in open(input_file, 'r'):
        if not line.isspace():
            result = line.strip()
            yield result.split(',')

def get_column(column, column_type):
    """Provides a column object to perform masking operations on"""

    customer = ColumnFactory()
    column = customer.return_object(column_type, column)
    return column

def mask_data(record, rules, mask):
    """Masks columns in a dataset given a mask and rules"""

    for heading, data in record.items():
        if isinstance(data, ColumnInterface): # Focus only on columns identified for masking by the user.
            data.mask(mask=mask, rules=rules)

def output(table, output):
    """Serialises the data back into a format specified by the user e.g. CSV or standard output"""

    serialise_customer = Outputs()
    csv = serialise_customer.get_serialiser("CSV", data=table, output_file=output)
    csv.serialise()
    stdout = serialise_customer.get_serialiser("STDOUT", data=table)
    stdout.serialise("Name", "Billing") # Column values to be printed to stdout

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    t1 = time.time()
    if input_file.lower().endswith(('csv')): # If file format is of csv
        customer_data = get_customers(input_file)
        output(customer_data, output_file)
        t2 = time.time()
        print(t2 - t1)
    else:
        raise ValueError(f"Invalid file input: {input_file}. Input file needs to be of CSV format")