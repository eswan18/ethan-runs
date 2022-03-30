import sys
import csv
import re
from datetime import datetime
import json

import requests

from app.schemas.activity import ActivityIn


def parse_date(d: str) -> datetime.date:
    '''
    Date values are stored in a non-standard format.

    All months are appreviated with three letters (e.g. Dec.) except September (Sept.)
    and months with names five letters and shorter (e.g. March), which don't even have
    a period in them.
    '''
    d = d.replace('.', '')
    # Keep only the first three letters of the month
    # (drop 't' from Sept, 'ch' from March)
    month, rest = d.split(' ', 1)
    d = month[:3] + ' ' + rest
    date = datetime.strptime(d, '%b %d, %Y').date()
    return date


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
        # Date values must be fixed.
        for key in ('date_submitted', 'workout_date'):
            date = parse_date(row_dict[key])
            row_dict[key] = date.strftime('%Y-%m-%d')
        # Some numeric values come in as empty strings but need to be null.
        for key in ('avg_heart_rate', 'steps'):
            if row_dict[key] == '':
                row_dict[key] = None
        j_str = json.dumps(row_dict)
        activity = ActivityIn.parse_raw(j_str)
        response = requests.post(f'{url}/activity', data=activity.json())
        print(response.status_code)
