import csv
import json
import os

CURRENT_DIR, filename = os.path.split(os.path.abspath(__file__))

reader = csv.reader(open('zipcode.csv', "rU"))
reader.next() # prime it

bulk_insert_list = []

for row in reader:
    zipcode, city, state, lat, long, timezone, dst = row

    entry = {
        'model': 'zipcodes.zipcode',
        'pk': zipcode,
        'fields': {
            'zipcode': zipcode,
            'city': city,
            'state': state,
            'longitude': long,
            'latitude': lat,
            'timezone': timezone,
            'dst': bool(dst),
        }
    }

    bulk_insert_list.append(entry)

fixtures_text = json.dumps(bulk_insert_list, sort_keys=True, indent=4, separators=(',', ': '))

with open(os.path.join(CURRENT_DIR, 'fixtures/initial.json'), 'w') as fixtures_file:
    fixtures_file.write(fixtures_text)