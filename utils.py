import numpy as np
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


def make_row(items):
    return ','.join(str(n) for n in items)
