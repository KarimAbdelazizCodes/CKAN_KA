import requests

# first I fetched all organizations with "all_fields" set to True, so I could get the organization ID
url = 'https://ckan.opendata.swiss/api/3/action/organization_list?all_fields=True'
res = requests.get(url)
organizations = res.json()['result']

# This object will just have the organization with the highest number of datasets
most_packages = {
    'org': '',
    'count': 0
}

"""
The below function loops over the fetched organizations, and for each organization, it will search for datasets 
created in 2020, where the owner_org ID matches with the ID passed in the url as a parameter.
"""

for organization in organizations:
    res = requests.get(f'https://ckan.opendata.swiss/api/3/action/package_search?q=owner_org:{organization["id"]}'
                       f'&fq=metadata_created:[2020-01-01T23:59:59.999Z TO 2020-12-31T00:00:00Z]')

    result = res.json()['result']

    if result['count'] > most_packages['count']:
        most_packages['count'] = result['count']
        most_packages['org'] = result['results'][0]['organization']['display_name']['de']

print(most_packages)  # prints {'org': 'Bundesamt für Statistik BFS', 'count': 866}

"""
'Bundesamt für Statistik BFS' had the most dataset entries in year 2020, with 866 datasets.
"""