
from functools import reduce

import numpy as np

from utils import get_repos_for_repo_search, make_row

API_SEARCH_BASE = "https://api.github.com/search/repositories"
OUTPUT_FILE = "js-report.csv"
QUERY_JS = "org:hmcts+language:javascript"
QUERY_TS = "org:hmcts+language:typescript"

get_repos = get_repos_for_repo_search(API_SEARCH_BASE)


def main():

    js_projects = np.array(list(get_repos(QUERY_JS)))
    ts_projects = np.array(list(get_repos(QUERY_TS)))
    concatenated = np.concatenate((js_projects, ts_projects))
    all_projects = [dict(t)
                    for t in {tuple(d.items()) for d in concatenated}]
    all_projects_sorted = sorted(all_projects, key=lambda item: item['name'])

    rows = list(map(
        lambda item: make_row([
            item['name'],
            'X' if (item in js_projects) else '',
            'X' if (item in ts_projects) else '',
            'X' if item['archived'] else ''
        ]),
        all_projects_sorted))

    np.savetxt(OUTPUT_FILE, rows,
               delimiter=',',
               fmt='%s',
               header='Project reference,JS,TS,Archived',
               comments='')

    print("Report saved: {}".format(OUTPUT_FILE))


if __name__ == '__main__':
    main()
