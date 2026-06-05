"""
This script was used to take a closer look at each of the columns
to look at the JSON key-value pairs and structure.
This script does not provide any use to the support of the backend
or the data as it was purely used for debugging purposes.
"""

import csv
import json

with open("backend/data/mil-cha-1-22-26.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["scoring"] and row["scoring"] != "null":
            print(json.dumps(
                json.loads(row["scoring"]),
                indent=4
            ))
            break