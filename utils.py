import csv

import requests


def get_repos_for_repo_search(api_search_base):
    def get_repos(query):
        url = "{}?q={}".format(api_search_base, query)
        data = requests.get(url).json()
        def lens(item): return {'name': item['name'],
                                'archived': item['archived']}
        return map(lens, data['items'])
    return get_repos

def get_repos_for_code_search(api_search_base):
    def get_repos(query):
        url = "{}?q={}".format(api_search_base, query)
        data = requests.get(url).json()
        def lens(item): return {'name': item['repository']['name']}
        return map(lens, data['items'])
    return get_repos

def save_csv(output_file, fieldnames, rows):
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Report saved: {}".format(output_file))
