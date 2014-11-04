import csv

def process_csv_format_file(file):
    """file is a file object that passed to csv reader, not a string of a file path"""
    reader = csv.reader(file)
    next(reader, None)  # returns the headers or `None` if the input is empty
    a=[]
    for row in reader:
        # as for the special file that I have now,
        a.append([float(x) for x in row[1:-3]])

