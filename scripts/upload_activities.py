import sys
import csv
import re
from datetime import datetime
import json

import requests

from app.schemas.activity import ActivityIn

DATE_FORMAT = '%b. %d, %Y'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('upload_activities: wrong number of arguments', file=sys.stderr)
        print('usage: python upload_activities [file] [url]', file=sys.stderr)
        sys.exit(1)
    filepath, url = sys.argv[1], sys.argv[2]

    with open(filepath, 'rt', newline='') as f:
        reader = csv.reader(f)
        row_iter = iter(reader)
        headers = next(row_iter)
        rows = [row for row in row_iter]

    # Normalize headers
    def normalize(s: str) -> str:
        # Pace (min/mile) => Pace (min per mile)
        s = s.replace('/', ' per ')
        # Pace (min per mile) => Pace in min per mile
        s = re.sub(r'\((.*)\)', r'in \1', s)
        s = s.lower().replace(' ', '_')
        return s
    headers = [normalize(h) for h in headers]

    # Create activities using this data and post them.
    for row in rows:
        row_dict = dict(zip(headers, row))
        # Date values are spelled out.
        for key in ('date_submitted', 'workout_date'):
            date = datetime.strptime(row_dict[key], DATE_FORMAT)
            row_dict[key] = date.strftime('%Y-%m-%d')
        j_str = json.dumps(row_dict)
        print(j_str)
        activity = ActivityIn.parse_raw(j_str)
        # activity = ActivityIn(**row_dict)
        print(activity)
        #response = requests.post(f'{url}/activity', data=activity.json())
        #print(response.status_code)
