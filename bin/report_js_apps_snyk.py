#!./env/bin/python

import numpy as np

from utils import (get_repos_for_code_search, get_repos_for_issues_search,
                   save_csv)

OUTPUT_FILE = "reports/js-apps-snyk-report.csv"
QUERY_ALL_JS = "org:hmcts+path:/+filename:package.json"
QUERY_WITH_SNYK = "org:hmcts+path:/+filename:package.json+snyk"
QUERY_WITH_NSP = "org:hmcts+path:/+filename:package.json+nsp"
QUERY_WITH_AUDIT = "org:hmcts+path:/+filename:package.json+'npm audit'"
QUERY_DEPENDABOT = "org:hmcts+dependabot"


def main():

    js_projects = np.array(list(get_repos_for_code_search(QUERY_ALL_JS)))
    js_projects_with_snyk = np.array(
        list(get_repos_for_code_search(QUERY_WITH_SNYK)))
    js_projects_with_nsp = np.array(
        list(get_repos_for_code_search(QUERY_WITH_NSP)))
    js_projects_with_audit = np.array(
        list(get_repos_for_code_search(QUERY_WITH_AUDIT)))
    js_projects_with_dependabot = np.array(
        list(get_repos_for_issues_search(QUERY_DEPENDABOT)))

    all_concatenated = np.concatenate((
        js_projects,
        js_projects_with_snyk,
        js_projects_with_nsp,
        js_projects_with_audit,
        js_projects_with_dependabot
    ))

    all_projects = [dict(t)
                    for t in {tuple(d.items()) for d in all_concatenated}]

    all_projects_sorted = sorted(all_projects, key=lambda item: item['name'])

    fieldnames = ['Reference', 'Uses Snyk', 'Uses deprecated nsp', 'npm audit', 'dependabot']

    def likely_node_app(item):
        return (item in concatenated_node_based_docker_projects) or (item in js_projects_with_express)

    rows = list(map(lambda item: {
        fieldnames[0]: item['name'],
        fieldnames[1]: 'X' if (item in js_projects_with_snyk) else '',
        fieldnames[2]: 'X' if (item in js_projects_with_nsp) else '',
        fieldnames[3]: 'X' if (item in js_projects_with_audit) else '',
        fieldnames[4]: 'X' if (item in js_projects_with_dependabot) else ''
    }, all_projects_sorted))

    save_csv(OUTPUT_FILE, fieldnames, rows)


if __name__ == '__main__':
    main()
