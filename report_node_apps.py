import numpy as np

from utils import get_repos_for_code_search, save_csv

API_SEARCH_BASE = "https://api.github.com/search/code"
OUTPUT_FILE = "node-apps-report.csv"
QUERY_WITH_EXPRESS = "org:hmcts+path:/+filename:package.json+express"
QUERY_ALL_JS = "org:hmcts+path:/+filename:package.json"
QUERY_NODE_BASED_DOCKER_IMAGE = "org:hmcts+path:/+filename:Dockerfile+node"
QUERY_NODE_BASED_DOCKER_IMAGE_2 = "org:hmcts+path:/+filename:Dockerfile+hmctspublic.azurecr.io/base/node"

get_repos = get_repos_for_code_search(API_SEARCH_BASE)


def main():

    js_projects = np.array(list(get_repos(QUERY_ALL_JS)))
    js_projects_with_express = np.array(list(get_repos(QUERY_WITH_EXPRESS)))

    node_based_docker_projects = np.array(list(get_repos(QUERY_NODE_BASED_DOCKER_IMAGE)))
    node_based_docker_projects_2 = np.array(list(get_repos(QUERY_NODE_BASED_DOCKER_IMAGE_2)))

    concatenated_node_based_docker_projects = np.concatenate((node_based_docker_projects, node_based_docker_projects_2))

    all_concatenated = np.concatenate((
        js_projects, 
        js_projects_with_express,
        concatenated_node_based_docker_projects
        ))

    all_projects = [dict(t)
                    for t in {tuple(d.items()) for d in all_concatenated}]
    all_projects_sorted = sorted(all_projects, key=lambda item: item['name'])

    fieldnames = ['Reference', 'Uses Express',  'Node-based docker image', 'Likely nodejs app']

    def likely_node_app(item):
        return (item in concatenated_node_based_docker_projects) or (item in js_projects_with_express)

    rows = list(map(lambda item: {
        fieldnames[0]: item['name'],
        fieldnames[1]: 'X' if (item in js_projects_with_express) else '',
        fieldnames[2]: 'X' if (item in concatenated_node_based_docker_projects) else '',
        fieldnames[3]: 'X' if likely_node_app(item) else ''
    }, all_projects_sorted))

    save_csv(OUTPUT_FILE, fieldnames, rows)


if __name__ == '__main__':
    main()
