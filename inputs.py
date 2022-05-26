class Inputs:
    def get_input(self, input_mode, input_file):
        if input_mode == "CSV":
            return CSVInput(input_file)
        else:
            raise ValueError(f"Invalid input format: {input_mode}")

class CSVInput():
    def __init__(self, input_file):
        self.input_file = input_file
        self.headings = None
        self.count = 0
        self.data = {}

    def _csvreader(self, input_file):
        for line in open(input_file, 'r'):
            if not line.isspace():
                result = line.strip()
                yield result.split(',')

    def get(self):
        reader = iter(self._csvreader(self.input_file))
        self.headings = next(reader) # this will be headings which will be ignored
        for heading in self.headings:
            if heading not in self.data:
                self.data[heading] = []
        for line in reader:
            self.count += 1
            i = 0
            for headings in self.data:
                self.data[headings].append(line[i])
                i += 1


