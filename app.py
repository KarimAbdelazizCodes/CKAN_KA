import requests
from datetime import datetime

baseurl = 'https://ckan.opendata.swiss/api/3/action/'

# first I fetched all organizations with "all_fields" set to True, so I could get the organization ID
res = requests.get(f'{baseurl}organization_list?all_fields=True')
organizations = res.json()['result']

"""
The below function loops over the fetched organizations, and for each organization, it will search for datasets 
created in 2020, where the owner_org ID matches with the ID passed in the url as a parameter.
"""

# This object will just have the organization with the highest number of datasets
most_packages = {
    'org': '',
    'count': 0
}

date_from = datetime.strptime('1 Jan 2020', '%d %b %Y').isoformat()
date_to = datetime.strptime('31 Dec 2020', '%d %b %Y').isoformat()

for organization in organizations:
    res = requests.get(f'{baseurl}package_search?q=owner_org:{organization["id"]}'
                       f'&fq=metadata_created:[{date_from}Z TO {date_to}Z]')

    result = res.json()['result']

    if result['count'] > most_packages['count']:
        most_packages['count'] = result['count']
        most_packages['org'] = result['results'][0]['organization']['display_name']['de']

print(most_packages)  # prints {'org': 'Bundesamt für Statistik BFS', 'count': 820}

"""
'Bundesamt für Statistik BFS' had the most dataset entries in year 2020, with 820 datasets.
"""
