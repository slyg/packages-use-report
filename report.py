
from functools import reduce

import numpy as np
import requests

API_SEARCH_BASE = "https://api.github.com/search/code"
OUTPUT_FILE = "gds-usage-report.csv"
QUERY_GDS = "org:hmcts+filename:package.json+govuk-frontend"
QUERY_GOV = "org:hmcts+filename:package.json+govuk-elements-sass"


def main():

    def repo_name_lens():
        return lambda i: i['repository']['full_name']

    def get_repos_for(query):
        url = "{}?q={}".format(API_SEARCH_BASE, query)
        data = requests.get(url).json()
        return map(repo_name_lens(), data['items'])

    gds_projects = np.array(get_repos_for(QUERY_GDS))
    gov_projects = np.array(get_repos_for(QUERY_GOV))
    intersection = np.intersect1d(gds_projects, gov_projects)
    all_projects = np.unique(np.concatenate((gds_projects, gov_projects)))

    def make_row(items):
        return ','.join(str(n) for n in items)

    def make_row_from_project_name(project_name):
        return make_row([
            project_name,
            'X' if (project_name in gds_projects) else '',
            'X' if (project_name in gov_projects) else '',
            'X' if (project_name in intersection) else ''
        ])

    rows = map(make_row_from_project_name, all_projects)

    np.savetxt(OUTPUT_FILE, rows,
               delimiter=',',
               fmt='%s',
               header='Project reference,Uses GDS,Uses deprecated gov-elements,Uses both',
               comments='')

    print("Report saved in {}".format(OUTPUT_FILE))


if __name__ == '__main__':
    main()
