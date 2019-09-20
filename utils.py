import requests


def get_repos_for_repo_search(api_search_base):
    def get_repos(query):
        url = "{}?q={}".format(api_search_base, query)
        data = requests.get(url).json()
        return map(
            lambda item: {'name': item['name'],
                          'archived': item['archived']},
            data['items'])
    return get_repos


def get_repos_for_code_search(api_search_base):
    def get_repos(query):
        url = "{}?q={}".format(api_search_base, query)
        data = requests.get(url).json()
        return map(
            lambda item: {'name': item['repository']['name']},
            data['items'])
    return get_repos


def make_row(items):
    return ','.join(str(n) for n in items)
