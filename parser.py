# encoding: utf-8

import copy
import datetime
import json

blacklisted_repos = []  # non-representative repos which alter stats

repos = {}
with open("github_repository_dump.json", 'rb') as f:
    repos = json.loads(f.read())
stats = {}  # get stats per repo
# simplicity over efficiency ahead...
for k, v in repos.items():
    total = sum(v["langs"].values()) * 1.0  # characters in each file
    ratios = {k: v / total for k, v in v["langs"].items()}
    stats[k] = {"lang": v["langs"], "lang_ratios": ratios}
    contribs = {}
    for c in v["contributors"]:
        first_contribution = min(w["w"] for w in c["weeks"] if w["c"])
        latest_contribution = max(w["w"] for w in c["weeks"] if w["c"])
        first_date = datetime.datetime.fromtimestamp(first_contribution)
        latest_date = datetime.datetime.fromtimestamp(latest_contribution)
        additions = sum(w["a"] for w in c["weeks"])
        deletions = sum(w["d"] for w in c["weeks"])
        contribs[c["author"]["login"]] = {
            "repos": 1,
            "additions": additions,
            "deletions": deletions,
            "contribs": additions + deletions,
            "net_contribs": additions - deletions,
            "commits": sum(w["c"] for w in c["weeks"]),
            "weeks_active": sum(1 for w in c["weeks"] if w["c"]),
            "period_contributed_in_days": (latest_date - first_date).days + 7,
            "first_contribution": first_contribution,
            "latest_contribution": latest_contribution,
        }
    total_commits = sum([c["commits"]for c in contribs.values()]) * 1.0
    total_additions = sum([c["additions"]for c in contribs.values()]) * 1.0
    total_deletions = sum([c["deletions"]for c in contribs.values()]) * 1.0
    total_contribs = total_additions + total_deletions
    total_net_contribs = total_additions - total_deletions
    for kk, vv in contribs.items():
        contribs[kk].update({
            "ratios": {
                "repos": 1,
                "commits": vv["commits"] / (total_commits or 1),
                "additions": vv["additions"] / (total_additions or 1),
                "deletions": vv["deletions"] / (total_deletions or 1),
                "contribs": vv["contribs"] / (total_contribs or 1),
                "net_contribs": vv["net_contribs"] / (total_net_contribs or 1),
            },
        })
    stats[k].update({
        "totals": {
            "repos": 1,
            "commits": total_commits,
            "additions": total_additions,
            "deletions": total_deletions,
            "contribs": total_contribs,
            "net_contribs": total_net_contribs,
        },
        "contributors": contribs,
    })

with open("stats_by_repo.json", 'w') as f:
    f.write(json.dumps(stats))

stats_by_user = {}  # get stats per user
language_counts = {
    "additions": 0,
    "deletions": 0,
    "contribs": 0,
    "commits": 0,
    "repos": 0
}
for stats_k, stats_v in stats.items():
    if stats_k in blacklisted_repos:
        continue
    for contrib_k, contrib_v in stats_v["contributors"].items():
        lang_stats = {lang: {} for lang in stats_v["lang_ratios"].keys()}
        for lang_k, lang_v in stats_v["lang_ratios"].items():
            for param in language_counts.keys():
                lang_stats[lang_k][param] = lang_v * contrib_v[param]
            lang_stats[lang_k]["repos"] = 1
        current_stats = stats_by_user.get(contrib_k)
        if not current_stats:  # every user's first time will be empty
            stats_by_user[contrib_k] = lang_stats
            continue
        for lang_k, lang_v in lang_stats.items():
            current_lang_stats = current_stats.get(lang_k)
            if not current_lang_stats:
                empty_language_counts = copy.deepcopy(language_counts)
                stats_by_user[contrib_k][lang_k] = empty_language_counts
                current_lang_stats = empty_language_counts
            for param in language_counts.keys():
                new_lang_stats = lang_v[param] + current_lang_stats[param]
                stats_by_user[contrib_k][lang_k][param] = new_lang_stats

with open("stats_by_user.json", 'w') as f:
    f.write(json.dumps(stats_by_user))
