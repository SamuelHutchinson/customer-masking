from column import ColumnInterface

class Outputs:
    """A class to determine the type of serialiser needed for a given output """

    def get_serialiser(self, serialiser_format, **kwargs):
        """Returns a serialiser based on the serialiser_format marked in the parameters"""

        if serialiser_format == "CSV":
            return CSVOutput(kwargs["data"], kwargs["output_file"])
        elif serialiser_format == "STDOUT":
            return STDOUTSerialiser(kwargs["data"])
        else:
            raise ValueError(f"Invalid serialiser: {serialiser_format}")

class CSVOutput:
    """A class to serialise data into CSV format"""

    def __init__(self, data, output_file):
        self.data = data.data.copy() # Create a copy so original isn't modified
        self.headings = data.headings
        self.count = data.count
        self.output_file = output_file

    def write(self):
        """outputs customer_data into a CSV file"""
        
        self._transform_data()
        with open(self.output_file, "w") as f:
            f.write(f"{','.join(map(str,self.headings))}\n") # write headings to file
            for i in range(self.count):
                record = [value[i] for value in self.data.values()]
                unpacked_row = ','.join(map(str, record))
                f.write(f"{unpacked_row}\n")
   
    def _transform_data(self):
        """finds any columns modified by the software and converts them back into lists ready to be persisted to a csv file"""
        for heading, data in self.data.items():
            if isinstance(data, ColumnInterface):
                self.data[heading] = data.values

class STDOUTSerialiser:
    """A class to serialise data into standard output, or in most cases print to the Command-Line Interface"""
    
    def __init__(self, data):
        self.data = data.data
    
    def write(self, *args):
        """Outputs column metrics requested by the user"""
        
        for column in args:
            print(f"{column}: Max. {self.data[column].maximum}, Min. {self.data[column].minimum} Avg. {self.data[column].average()}")
