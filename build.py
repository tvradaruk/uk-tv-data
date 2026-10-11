#!/usr/bin/env python3
"""Rebuild this dataset from the TV Radar working repo.

    python build.py                       # default source: ../035-tvradarwordpress
    python build.py --src <path to repo>

Only aggregates and public facts are published here: channel numbers, and
counts of airings per channel and per title. No programme listings, synopses
or schedules are copied, because the listings themselves are third-party data.
"""
import argparse
import csv
import glob
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

# Channel-table names that differ from the pillar slug.
PILLAR_ALIASES = {
    "itv1 (stv in scotland, utv in northern ireland)": "itv1",
    "channel 4 (s4c in wales)": "channel-4",
    "bbc four (channel 24 in scotland, where 9 carries bbc scotland)": "bbc-four",
    "u&dave": "dave",
    "u&drama": "drama",
    "u&yesterday": "yesterday",
    "great! christmas": "great-romance",
    "that's tv": "thats-tv",
    "talking pictures tv": "talking-pictures",
}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("!", "")).strip("-")


def pillars(src):
    return {os.path.basename(p)[: -len("-tv-guide.md")]
            for p in glob.glob(os.path.join(src, "content/tv-guide/channels/*-tv-guide.md"))}


def channel_numbers(src):
    page = open(os.path.join(src, "content/pages/freeview-channel-guide.md"), encoding="utf-8").read()
    known = pillars(src)
    rows = []
    for m in re.finditer(r"^\| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", page, re.M):
        lcn, name, operator, hd = (g.strip() for g in m.groups())
        key = PILLAR_ALIASES.get(name.lower(), slugify(name))
        url = f"https://tvradar.uk/{key}-tv-guide" if key in known else ""
        rows.append({"lcn": int(lcn), "channel": name, "operator": operator,
                     "hd_on_freeview": "yes" if "✅" in hd else "no", "tvradar_guide": url})
    if len(rows) < 40:
        raise SystemExit(f"only {len(rows)} channel rows parsed; the page table changed")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(HERE, "..", "035-tvradarwordpress"))
    src = os.path.abspath(ap.parse_args().src)

    os.makedirs(os.path.join(HERE, "freeview"), exist_ok=True)
    rows = channel_numbers(src)
    with open(os.path.join(HERE, "freeview", "freeview-channel-numbers.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"freeview-channel-numbers.csv: {len(rows)} channels, "
          f"{sum(1 for r in rows if r['tvradar_guide'])} linked to a guide")

    os.makedirs(os.path.join(HERE, "repeats"), exist_ok=True)
    for path in glob.glob(os.path.join(src, "data", "repeats-by-*.csv")):
        shutil.copy(path, os.path.join(HERE, "repeats", os.path.basename(path)))
        print(f"repeats/{os.path.basename(path)}")


if __name__ == "__main__":
    main()
