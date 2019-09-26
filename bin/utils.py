import json
from csv import DictWriter
from hashlib import md5
from os.path import exists
from time import sleep

from requests import get

API_CODE_SEARCH_BASE = "https://api.github.com/search/code"
API_REPO_SEARCH_BASE = "https://api.github.com/search/repositories"
API_ISSUES_SEARCH_BASE = "https://api.github.com/search/issues"


def get_repos_for_repo_search(query):

    cache_file = get_cache_file_name(query)

    if (exists(cache_file)):
        data = json.loads(read_cache(cache_file))

    else:
        token = get_auth_token()
        url = "{}?q={}".format(API_REPO_SEARCH_BASE, query)
        prevent_rate_limit()
        data = get(url, headers={"Authorization": "token {}".format(token)}).json()
        write_cache(cache_file, json.dumps(data))

    def lens(item): return {'name': item['name'],
                            'archived': item['archived']}

    return map(lens, data['items'])

def get_repos_for_code_search(query):

    cache_file = get_cache_file_name(query)

    if (exists(cache_file)):
        data = json.loads(read_cache(cache_file))

    else:
        token = get_auth_token()
        url = "{}?q={}".format(API_CODE_SEARCH_BASE, query)
        prevent_rate_limit()
        data = get(url, headers={"Authorization": "token {}".format(token)}).json()
        write_cache(cache_file, json.dumps(data))
    
    def lens(item): return {'name': item['repository']['name']}
    return map(lens, data['items'])

def get_repos_for_issues_search(query):

    cache_file = get_cache_file_name(query)

    if (exists(cache_file)):
        data = json.loads(read_cache(cache_file))

    else:
        token = get_auth_token()
        url = "{}?q={}".format(API_ISSUES_SEARCH_BASE, query)
        prevent_rate_limit()
        data = get(url, headers={"Authorization": "token {}".format(token)}).json()
        write_cache(cache_file, json.dumps(data))

    def lens(item): return {'name': item['repository_url'].rsplit('/', 1)[1]}
    return map(lens, data['items'])

def get_auth_token():
    file = open('auth', mode='r')
    token = file.read()
    file.close()
    return token

def write_cache(output_file, payload):
    with open(output_file, 'w', newline='') as f:
        f.write(payload)
        f.close()

def read_cache(input_file):
    with open(input_file, 'r') as f:
        content = f.read()
        f.close()
    return content

def save_csv(output_file, fieldnames, rows):
    with open(output_file, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Report saved: {}".format(output_file))

def get_cache_file_name(query):
    h = md5()
    h.update(query.encode('utf-8'))
    query_hash = h.hexdigest()
    return 'reports/{}.json'.format(query_hash)

def prevent_rate_limit():
    sleep(1)
