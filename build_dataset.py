#!/usr/bin/env python3
"""Validate facts.json and rebuild facts.csv and the fact count in README.md.

facts.json is the source of truth. Run this after editing it:

    python3 build_dataset.py           # validate, sort by id, rewrite facts.json, facts.csv and README count
    python3 build_dataset.py --check   # validate only; exit 1 if anything is invalid or out of date

Standard library only (Python 3.8 or newer).
"""
import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACTS_JSON = ROOT / "facts.json"
FACTS_CSV = ROOT / "facts.csv"
README = ROOT / "README.md"

FIELDS = ["id", "fact", "category", "source_title", "source_url", "article_url", "added"]
CATEGORIES = {"anatomy", "behavior", "history", "breeds", "genetics", "records", "culture", "science"}
SITE = "https://cattriviagames.com/"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# characters the dataset never uses: em dash, en dash, and emoji or pictographs
BANNED_RE = re.compile("[\u2013\u2014\u2600-\u27bf\U0001f000-\U0001faff\ufe0f]")
COUNT_RE = re.compile(r"(<!-- count -->)(\d+)(<!-- /count -->)")


def validate(facts):
    """Return a list of problems; an empty list means the data is valid."""
    problems = []
    if not isinstance(facts, list):
        return ["facts.json must hold a JSON array"]
    seen_ids, seen_facts = set(), set()
    for n, item in enumerate(facts):
        where = f"entry {n}"
        if not isinstance(item, dict):
            problems.append(f"{where}: not an object")
            continue
        where = f"entry {n} ({item.get('id', '?')})"
        missing = [f for f in FIELDS if f not in item]
        extra = [f for f in item if f not in FIELDS]
        if missing:
            problems.append(f"{where}: missing {', '.join(missing)}")
        if extra:
            problems.append(f"{where}: unknown field {', '.join(extra)}")
        for f in FIELDS:
            v = item.get(f)
            if f in item and (not isinstance(v, str) or not v.strip() or v != v.strip()):
                problems.append(f"{where}: {f} must be a non-empty trimmed string")
        if missing or extra:
            continue
        fid, fact = item["id"], item["fact"]
        if not ID_RE.match(fid) or len(fid) > 80:
            problems.append(f"{where}: id must be a lowercase slug of at most 80 characters")
        if fid in seen_ids:
            problems.append(f"{where}: duplicate id")
        seen_ids.add(fid)
        if fact.lower() in seen_facts:
            problems.append(f"{where}: duplicate fact")
        seen_facts.add(fact.lower())
        if not 20 <= len(fact) <= 320:
            problems.append(f"{where}: fact should be 20 to 320 characters")
        if not re.search(r'[.!?]["”]?$', fact):
            problems.append(f"{where}: fact must be one full sentence ending in a period")
        if "  " in fact or "\n" in fact:
            problems.append(f"{where}: fact has a double space or line break")
        for f in ("fact", "source_title"):
            if BANNED_RE.search(item[f]):
                problems.append(f"{where}: {f} contains an em dash, en dash or emoji")
        if item["category"] not in CATEGORIES:
            problems.append(f"{where}: category must be one of {', '.join(sorted(CATEGORIES))}")
        if not re.match(r"^https?://[^\s]+$", item["source_url"]):
            problems.append(f"{where}: source_url must be an http(s) URL")
        if item["source_url"].startswith(SITE):
            problems.append(f"{where}: source_url must be the outside source, not a cattriviagames.com page")
        if not item["article_url"].startswith(SITE) or " " in item["article_url"]:
            problems.append(f"{where}: article_url must start with {SITE}")
        if not DATE_RE.match(item["added"]):
            problems.append(f"{where}: added must be a YYYY-MM-DD date")
    return problems


def render_json(facts):
    return json.dumps(facts, indent=2, ensure_ascii=False) + "\n"


def render_csv(facts):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for item in facts:
        writer.writerow({f: item[f] for f in FIELDS})
    return buf.getvalue()


def render_readme(text, count):
    if not COUNT_RE.search(text):
        raise SystemExit("README.md is missing the <!-- count -->N<!-- /count --> marker")
    return COUNT_RE.sub(lambda m: f"{m.group(1)}{count}{m.group(3)}", text)


def main(argv):
    check_only = "--check" in argv
    try:
        facts = json.loads(FACTS_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        print(f"Cannot read facts.json: {err}")
        return 1
    problems = validate(facts)
    if problems:
        print(f"{len(problems)} problem(s) in facts.json:")
        for p in problems[:50]:
            print("  " + p)
        return 1

    facts = sorted(facts, key=lambda x: x["id"])
    outputs = {
        FACTS_JSON: render_json(facts),
        FACTS_CSV: render_csv(facts),
        README: render_readme(README.read_text(encoding="utf-8"), len(facts)),
    }
    stale = [p.name for p, body in outputs.items()
             if not p.exists() or p.read_text(encoding="utf-8") != body]
    by_cat = Counter(x["category"] for x in facts)
    summary = ", ".join(f"{c} {by_cat[c]}" for c in sorted(by_cat))
    if check_only:
        if stale:
            print("Out of date: " + ", ".join(stale) + ". Run python3 build_dataset.py and commit the result.")
            return 1
        print(f"OK: {len(facts)} facts ({summary}); facts.csv and README.md are up to date.")
        return 0
    for path, body in outputs.items():
        path.write_text(body, encoding="utf-8")
    print(f"Wrote {len(facts)} facts ({summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
