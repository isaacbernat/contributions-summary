# contributions-summary
Get stats and a summary of your contributions in GitHub repositories via github API.

This is a playful exercise to get an approximate overview of how much contributions each developer makes into specific repositories, how are your contributions shared amoung differents languages, etc. The method used to get the exact numbers is an approximation;

## How it works
1. `python scraper.py`
2. `python parser.py`
3. enjoy the created json files!

### Samples
```python
pprint(stats_by_user["isaacbernat"])

{  # commented out most languages to make it shorter
 u'Dart': {
    'additions': 6118.204211656423,
    'commits': 134.00782717426114,
    'contribs': 9944.069807743856,
    'deletions': 3825.865596087434,
    'repos': 3},
 u'Go': {
    'additions': 13347.344324309803,
    'commits': 396.7234329031459,
    'contribs': 20823.853041330956,
    'deletions': 7476.508717021151,
    'repos': 11},
 u'JavaScript': {
    'additions': 22728.76281277121,
    'commits': 184.06109486711617,
    'contribs': 27449.19300021827,
    'deletions': 4720.430187447064,
    'repos': 6},
 u'Python': {
    'additions': 13486.98261503414,
    'commits': 413.6388680916634,
    'contribs': 20630.775081585376,
    'deletions': 7143.792466551241,
    'repos': 27},
```

```python
pprint(stats["pycrastinate"])

{'contributors': {
    u'grafuls': {
        'additions': 4,
        'commits': 1,
        'contribs': 9,
        'deletions': 5,
        'first_contribution': 1433030400,
        'latest_contribution': 1433030400,
        'net_contribs': -1,
        'period_contributed_in_days': 7,
        'ratios': {
            'additions': 0.0015390534821085034,
            'commits': 0.011111111111111112,
            'contribs': 0.0025495750708215297,
            'deletions': 0.0053705692803437165,
            'net_contribs': -0.0005995203836930455,
            'repos': 1},
        'repos': 1,
        'weeks_active': 1},
    u'isaacbernat': {
        'additions': 2595,
        'commits': 89,
        'contribs': 3521,
        'deletions': 926,
        'first_contribution': 1394323200,
        'latest_contribution': 1408838400,
        'net_contribs': 1669,
        'period_contributed_in_days': 175,
        'ratios': {
            'additions': 0.9984609465178915,
            'commits': 0.9888888888888889,
            'contribs': 0.9974504249291785,
            'deletions': 0.9946294307196563,
            'net_contribs': 1.000599520383693,
            'repos': 1},
        'repos': 1,
        'weeks_active': 18}},
 'lang': {u'Python': 47331, u'Ruby': 91},
 'lang_ratios': {u'Python': 0.9980810594238961, u'Ruby': 0.001918940576103918},
 'totals': {'additions': 2599.0,
            'commits': 90.0,
            'contribs': 3530.0,
            'deletions': 931.0,
            'net_contribs': 1668.0,
            'repos': 1}}
```

### Disclaimers
- Since we use github API, it means there is a rate limit of 5000 requests. If you have thousands of repositories this tool may present problems.

- The way ratios are calculated is the following:
    - We get the language data from GitHub. It gives the number of characters each file has and assigns those character values to a language. Also it's non-obvious how some files like Readmes are catalogues as different programming languages.
    - A ratio is calculated for each language according to the weight given by GitHub.
    - The commit we get from github for each contributor is grouped by week.
    - We only get number of commits, lines added and lines removed for each developer and week.
    - Therefore, we assume the language ratio of each contribution is the same as the global ratio.
    - We also assume that each line of code is as long as the average.
    - We can't distinguish when code is just moved around, etc.

## TODOs:
- Filter stats to just take into account commits before or after some date
- Create a version to scan through all commits (so we can get exact real and not approximate data)
- More stats
- Refactor this into functions
- Assemble a version for Pip
