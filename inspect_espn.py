#!/usr/bin/env python3
"""Fetch ESPN Valero Texas Open data and inspect round/hole structure."""
import json
import urllib.request

URL = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/scoreboard"
TOURNAMENT_ID = "401811940"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

# Find the Valero event
event = None
for e in data.get("events", []):
    if e.get("id") == TOURNAMENT_ID:
        event = e
        break
if not event:
    for e in data.get("events", []):
        event = e
        break

if not event:
    print("No event found!")
    exit(1)

print(f"Event: {event.get('name')}")
print(f"Event status: {json.dumps(event.get('status', {}), indent=2)}")
print()

comp = event.get("competitions", [{}])[0]
competitors = comp.get("competitors", [])
print(f"Total competitors: {len(competitors)}")
print()

# Show first 5 active players and first 2 cut players
active_shown = 0
cut_shown = 0

for p in sorted(competitors, key=lambda x: x.get("order", 999)):
    name = p.get("athlete", {}).get("displayName", "?")
    score = p.get("score", "?")
    status = p.get("status", {})
    ls = p.get("linescores", [])

    is_cut = score in ("CUT", "cut")
    is_wd = score in ("WD", "wd")

    if is_cut:
        if cut_shown >= 2:
            continue
        cut_shown += 1
    elif is_wd:
        continue
    else:
        if active_shown >= 5:
            continue
        active_shown += 1

    print(f"{'='*60}")
    print(f"Player: {name}")
    print(f"Score: {score}")
    print(f"Status: {json.dumps(status, indent=2)}")
    print(f"Linescores count: {len(ls)}")

    for i, rd in enumerate(ls):
        rd_holes = rd.get("linescores", [])
        print(f"  Round {i+1}: displayValue={rd.get('displayValue', '?')}, "
              f"value={rd.get('value', '?')}, "
              f"period={rd.get('period', '?')}, "
              f"holes_data_count={len(rd_holes)}")
    print()

    if active_shown >= 5 and cut_shown >= 2:
        break

# Summary stats
print(f"\n{'='*60}")
print("SUMMARY: Round hole data availability")
for rnd in range(4):
    players_with_holes = 0
    players_with_18 = 0
    players_with_score = 0
    active_count = 0
    for p in competitors:
        score = p.get("score", "")
        if score in ("CUT", "cut", "WD", "wd"):
            continue
        active_count += 1
        ls = p.get("linescores", [])
        if rnd < len(ls):
            rd = ls[rnd]
            if rd.get("displayValue"):
                players_with_score += 1
            holes = rd.get("linescores", [])
            if len(holes) > 0:
                players_with_holes += 1
            if len(holes) == 18:
                players_with_18 += 1
    print(f"  R{rnd+1}: active={active_count}, with_score={players_with_score}, "
          f"with_any_holes={players_with_holes}, with_18_holes={players_with_18}")
