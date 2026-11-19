"""Scrape the public contribution calendar for USER into data/contributions.json."""
import json, os, re, datetime, urllib.request
USER = os.environ.get("GH_USER", "JorJamess")
html = urllib.request.urlopen(urllib.request.Request(
    f"https://github.com/users/{USER}/contributions", headers={"User-Agent": "readme-cards"}), timeout=30).read().decode()
levels = sorted(set(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?data-level="(\d)"', html)))
counts = {}
for t, d in re.findall(r'(No contributions|\d+ contributions?) on ([A-Za-z]+ \d+)', html):
    counts[d] = 0 if t[0] == "N" else int(t.split()[0])
days = []
for dt, lv in levels:
    x = datetime.date.fromisoformat(dt)
    days.append([dt, lv, counts.get(x.strftime("%B ") + str(x.day), 0)])
assert len(days) > 300, "calendar scrape looks wrong; keeping old data"
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
json.dump({"days": days, "total": sum(d[2] for d in days)}, open(os.path.join(root, "data/contributions.json"), "w"))
print("days", len(days))
