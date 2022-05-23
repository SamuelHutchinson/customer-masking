from column import ColumnInterface

class SerialiseCustomer:
    """A class to determine the type of serialiser needed for a given output """

    def get_serialiser(self, serialiser_format, **kwargs):
        """Returns a serialiser based on the serialiser_format marked in the parameters"""

        if serialiser_format == "CSV":
            return CSVSerialiser(kwargs["data"], kwargs["output_file"])
        elif serialiser_format == "STDOUT":
            return STDOUTSerialiser(kwargs["data"])
        else:
            raise ValueError(f"Invalid serialiser: {serialiser_format}")

class CSVSerialiser:
    """A class to serialise data into CSV format"""

    def __init__(self, data, output_file):
        self.data = data.copy() # Create a copy so original isn't modified
        self.output_file = output_file

    def serialise(self):
        """Serialises data into a 2D List then outputs contents into a CSV file"""
        
        self._transform_data()
        result = []
        result.append(self.data.keys()) # Column headings go first
        values = list(self.data.values()) # Then followed by the actual data
        no_of_rows = len(values[0]) # Get number of rows in dataset by obtaining length of first column
        for i in range(no_of_rows):
            record = [value[i] for value in values]
            result.append(record)
        with open(self.output_file, "w") as f:
            for row in result:
                unpacked_row = ','.join(map(str, row))
                f.write(f"{unpacked_row}\n")
    
    def _transform_data(self):
        """finds any columns modified by the software and converts them back into lists ready to be persisted to a csv file"""

        for heading, data in self.data.items():
            if isinstance(data, ColumnInterface):
                self.data[heading] = data.values

class STDOUTSerialiser:
    """A class to serialise data into standard output, or in most cases print to the Command-Line Interface"""
    
    def __init__(self, data):
        self.data = data
    
    def serialise(self, *args):
        """Outputs column metrics requested by the user"""
        
        for column in args:
            print(f"{column}: Max. {self.data[column].maximum}, Min. {self.data[column].minimum} Avg. {self.data[column].average()}")
