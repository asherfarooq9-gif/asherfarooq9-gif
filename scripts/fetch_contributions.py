import json, os, urllib.request
user = os.environ.get("GH_USER", "asherfarooq9-gif")
q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}' % user
req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": q}).encode(),
    {"Authorization": "bearer " + os.environ["GH_TOKEN"], "Content-Type": "application/json"})
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days = [{"date": d["date"], "count": d["contributionCount"]} for w in cal["weeks"] for d in w["contributionDays"]]
json.dump({"total": cal["totalContributions"], "days": days}, open("data/contributions.json", "w"))
