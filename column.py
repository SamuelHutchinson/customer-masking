class ColumnFactory():
    """A class to determine the type of Column and what object it should return"""

    def return_object(self, column_type, data):
        """Returns a column object based on column_type marked by the user"""

        if column_type == "Numeric":
            return NumericColumn(data)
        elif column_type == "Alphanumeric":
            return AlphanumericColumn(data)
        else:
            raise ValueError(f"Invalid Column type: {column_type}")

class ColumnInterface:
    """A common interface for any columns being masked"""
    
    pass

class NumericColumn(ColumnInterface):
    """A class used to parse a column containing purely numerical data"""

    def __init__(self, values):
        self.values = self._get_values(values)
        # Obtain min/max values before any masking takes place
        self.minimum = min(self.values)
        self.maximum = max(self.values)

    def _get_values(self, values):
        """Ensures all field values in a column are actually numerical"""

        result = []
        for value in values:
            try:
                # If a value is wholly numeric e.g. 12345 convert to float or if no data present put a 0.0 in its place
                result.append(float(value.strip(' ') or 0))
            except:
                # If a value is NOT wholly numeric and/or is malformed e.g. 12345abc
                # then leave it out of the dataset and replace with 0.0 to reduce data contamination
                result.append(0.0)
        return result

    def mask(self, **kwargs):
        """Performs masking operations on the column"""

        string_values = list(map(str, self.values)) # Converts all field values to string
        average = str(self.average())
        masked_values = [value.replace(value, average) for value in string_values]
        # Convert back to float so further numerical operations can be applied for it if needed.
        self.values = list(map(float, masked_values))

    def average(self):
        """Calculate average value of field values for the entire dataset"""

        return sum(self.values) / len(self.values)

class AlphanumericColumn(ColumnInterface):
    """A class used to parse a column with data containing all characters and not just numbers"""

    def __init__(self, values):
        self.values = values
        # Retrieve max and min values
        self.value_lengths = list(map(len, self.values)) # Replace field values with their respective lengths for numerical ops
        self.minimum = min(self.value_lengths)
        self.maximum = max(self.value_lengths)

    def mask(self, **kwargs):
        """Performs masking operations on the column"""

        mask = kwargs["mask"]
        rules = kwargs['rules']
        # Apply mask and rules to the provided dataset
        self.values = [self._mask_value(value, mask, rules) for value in self.values]


    def _mask_value(self, value, mask, rules):
        """Applies masking on a field value using rules such as symbols/characters to be excluded"""

        for letter in value:
            if letter == mask: continue # Do nothing
            elif letter not in rules: # Mask the letter in the field value
                value = value.replace(letter, mask)
        return value

    def average(self):
        """Calculate average length of field values in the entire dataset"""

        return sum(self.value_lengths) / len(self.value_lengths)
