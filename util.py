import csv

def extract(csv_string):
    data = []
    reader = csv.DictReader(csv_string.splitlines())
    for row in reader:
        data.append(row)
    print(data)
    return data