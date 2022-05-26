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
        self.values = values
        self.minimum = None
        self.maximum = None

    def mask(self, **kwargs):
        """Performs masking operations on the column"""

        self._convert_values()
        average = self.average()
        for i in range(len(self.values)):
            self.values[i] = average

    def _convert_values(self):
        for i in range(len(self.values)):
            try:
                self.values[i] = float(self.values[i].strip(' ') or 0)
            except:
                self.values[i] = 0.0
        self.minimum = min(self.values)
        self.maximum = max(self.values)

    def average(self):
        """Calculate average value of field values for the entire dataset"""
        return sum(self.values) / len(self.values)

class AlphanumericColumn(ColumnInterface):
    """A class used to parse a column with data containing all characters and not just numbers"""

    def __init__(self, values):
        self.values = values
        # Retrieve max and min values
        self.minimum = len(min(self.values, key=len))
        self.maximum = len(max(self.values, key=len))

    def mask(self, **kwargs):
        """Performs masking operations on the column"""

        mask = kwargs["mask"]
        rules = kwargs['rules']
        # Apply mask and rules to the provided dataset
        for i in range(len(self.values)):
            self.values[i] = self._mask_value(self.values[i], mask, rules)

    def _mask_value(self, value, mask, rules):
        """Applies masking on a field value using rules such as symbols/characters to be excluded"""
        for letter in value:
            if letter not in rules: # Mask the letter in the field value
                value = value.replace(letter, mask, 1)
        return value

    def average(self):
        """Calculate average length of field values in the entire dataset"""
        value_lengths = list(map(len, self.values))
        return sum(value_lengths) / len(value_lengths)
