
from functools import reduce

import numpy as np
from utils import get_repos_for_code_search, make_row

API_SEARCH_BASE = "https://api.github.com/search/code"
OUTPUT_FILE = "gds-usage-report.csv"
QUERY_GDS = "org:hmcts+filename:package.json+govuk-frontend"
QUERY_GOV = "org:hmcts+filename:package.json+govuk-elements-sass"

get_repos = get_repos_for_code_search(API_SEARCH_BASE)


def main():

    gds_projects = np.array(get_repos(QUERY_GDS))
    gov_projects = np.array(get_repos(QUERY_GOV))
    intersection = np.intersect1d(gds_projects, gov_projects)
    all_projects = np.unique(np.concatenate((gds_projects, gov_projects)))

    def make_row_from_project_name(item):
        return make_row([
            item['name'],
            'X' if (item in gds_projects) else '',
            'X' if (item in gov_projects) else '',
            'X' if (item in intersection) else ''
        ])

    rows = map(make_row_from_project_name, all_projects)

    np.savetxt(OUTPUT_FILE, rows,
               delimiter=',',
               fmt='%s',
               header='Project reference,Uses GDS,Uses deprecated gov-elements,Uses both',
               comments='')

    print("Report saved: {}".format(OUTPUT_FILE))


if __name__ == '__main__':
    main()
