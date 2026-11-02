#!/usr/bin/env python3
"""Print a random cat fact with its source and the required credit line.

Python 3.8 or newer, standard library only.

    python3 examples/random_fact.py
    python3 examples/random_fact.py --category genetics
    python3 examples/random_fact.py --file facts.json     (read a local copy instead of the CDN)
"""
import argparse
import json
import random
import sys
import urllib.request

DATA_URL = "https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.json"
CREDIT = "Cat facts from Cat Trivia Games, https://cattriviagames.com, CC BY 4.0"
CATEGORIES = ["anatomy", "behavior", "history", "breeds", "genetics", "records", "culture", "science"]


def load_facts(path=None, url=DATA_URL):
    if path:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    request = urllib.request.Request(url, headers={"User-Agent": "cat-facts-dataset-example"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def pick_fact(facts, category=None):
    pool = [f for f in facts if f["category"] == category] if category else facts
    return random.choice(pool) if pool else None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print a random cat fact.")
    parser.add_argument("--category", "-c", choices=CATEGORIES, help="only pick from this category")
    parser.add_argument("--file", "-f", help="read a local facts.json instead of the CDN copy")
    parser.add_argument("--url", default=DATA_URL, help="where to load facts.json from")
    args = parser.parse_args(argv)
    try:
        facts = load_facts(args.file, args.url)
    except (OSError, ValueError) as err:
        print(f"Could not load the facts: {err}", file=sys.stderr)
        return 1
    fact = pick_fact(facts, args.category)
    if not fact:
        print("No facts found.", file=sys.stderr)
        return 1
    print(fact["fact"])
    print()
    print(f"Category: {fact['category']}")
    print(f"Source:   {fact['source_title']} <{fact['source_url']}>")
    print(f"Article:  {fact['article_url']}")
    print()
    print(CREDIT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
