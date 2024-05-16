import csv

class CSVWriter:
    def __init__(self, filename, fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL):
        self.filename = filename
        self.fieldnames = fieldnames
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.quoting = quoting
        self.file = None
        self.writer = None
        
    def open(self):
        """Open the CSV file and prepare it for writing."""
        self.file = open(self.filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames, delimiter=self.delimiter, 
                                     quotechar=self.quotechar, quoting=self.quoting)
        self.writer.writeheader()
        
    def write_row(self, row):
        """Write a single row to the CSV file."""
        if self.writer:
            self.writer.writerow(row)
        else:
            raise Exception("CSV file is not open. Call the open() method before writing.")
            
    def write_rows(self, rows):
        """Write multiple rows to the CSV file."""
        for row in rows:
            self.write_row(row)
            
    def close(self):
        """Close the CSV file."""
        if self.file:
            self.file.close()
        self.file = None
        self.writer = None

