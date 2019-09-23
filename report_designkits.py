
from functools import reduce

import numpy as np

from utils import get_repos_for_code_search, make_row

API_SEARCH_BASE = "https://api.github.com/search/code"
OUTPUT_FILE = "gds-usage-report.csv"
QUERY_GDS = "org:hmcts+filename:package.json+govuk-frontend"
QUERY_GOV = "org:hmcts+filename:package.json+govuk-elements-sass"

get_repos = get_repos_for_code_search(API_SEARCH_BASE)


def main():

    gds_projects = np.array(list(get_repos(QUERY_GDS)))
    gov_projects = np.array(list(get_repos(QUERY_GOV)))
    names_in_gov_projects = {gds_projects['name']
                             for gds_projects in gov_projects}
    intersection = [d for d in gds_projects if d['name']
                    in names_in_gov_projects]
    concatenated = np.concatenate((gds_projects, gov_projects))
    all_projects = [dict(t)
                    for t in {tuple(d.items()) for d in concatenated}]
    all_projects_sorted = sorted(all_projects, key=lambda item: item['name'])

    rows = list(map(lambda item: make_row([
        item['name'],
        'X' if (item in gds_projects) else '',
        'X' if (item in gov_projects) else '',
        'X' if (item in intersection) else ''
    ]), all_projects_sorted))

    np.savetxt(OUTPUT_FILE, rows,
               delimiter=',',
               fmt='%s',
               header='Project reference,Uses GDS,Uses deprecated gov-elements,Uses both',
               comments='')

    print("Report saved: {}".format(OUTPUT_FILE))


if __name__ == '__main__':
    main()
