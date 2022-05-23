# Customer Masking
A python application for the masking of sensitive customer data
## Contents
* README.md
    * Tells a bit more about the program as well as instructions for how to run it too. 
* customer_masking.py
    * Entry point for the application
    * Extracts data from input file, masks columns specified by user and also outputs the masked data
* column.py
    * Contains models for the two types of columns that can be present in data: NumericColumn and AlphanumericColumn
    * ColumnFactory, for returning the correct column object based on the column_type a user has mapped to a column
    * ColumnInterface, a single entity for interacting with all different types of column, including existing implementations and any built in the future
* serialisers.py
    * For serialising data to an output of a programmer's choice
    * Two implementations: CSVSerialiser and STDOUTSerialiser. Programmer can add more as scope changes e.g. JSONSerialiser for serialising masked data to JSON if needed. 
    * SerialiseCustomer, a factory for returning the correct serialiser object based on the serialiser_format requested by a programmer. Similar to the above point, it can be extended to accomodate more or different serialisers as needed.
* customers.csv, test1.csv, test3.csv
    * Contains testing data to run the program against

## Assumptions
* 'Letter Appearances on alphanumeric columns' means any character in field values except spaces, masking as much as possible ensures field values remain anonymous!
* Spaces in field values won't be masked because of this
* Numbers in numeric columns are parsed as floats to preserve granularity of data
* Erroneous or missing data in numeric columns are to be replaced with 0.0 so original data doesn't contaminate metrics such as min/max values and averages
* Missing data in Alphanumeric columns will not be masked or replaced with anything and will remain blank

## Running the code
```
python3 customer_masking.py [input] [output]
```
[input] is the source containing input data and is a required argument. [output] is an optional argument for persisting masked data to a file

The software has been written to take in only CSV files for now:
```
python3 customer_masking.py customers.csv masked_clients.csv
```
The program of course can be extended to support other files types when needed!