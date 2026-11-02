# Cat facts dataset

An open set of <!-- count -->290<!-- /count --> short cat facts, each one a single sentence with the outside source it comes from. The facts are drawn from articles published on [Cat Trivia Games](https://cattriviagames.com), and every fact links back to the article that states it and to the source that article cites.

The files are plain JSON and CSV, free to use in apps, bots, quizzes, classrooms and research under the Creative Commons Attribution 4.0 license.

## Files

| File | What it holds |
| --- | --- |
| `facts.json` | All facts as a JSON array. This is the source of truth. |
| `facts.csv` | The same facts as UTF-8 CSV with a header row. |
| `build_dataset.py` | Checks `facts.json` and rebuilds `facts.csv` and the count above. |
| `examples/random-fact.js` | Prints a random fact with the credit line (Node 18 or newer). |
| `examples/random_fact.py` | The same in Python 3, standard library only. |
| `index.html` | A one-page random fact viewer for GitHub Pages. |
| `LICENSE` (the full CC BY 4.0 legal code) and `NOTICE.md` (copyright and a plain-language summary) | The license summary and a link to the full legal code. |

## Fields

Each fact is an object with these fields, all strings:

| Field | Meaning |
| --- | --- |
| `id` | A stable slug, such as `kittens-open-eyes-days-old`. It does not change if the wording of the fact is corrected, so you can store it. |
| `fact` | One standalone sentence. |
| `category` | One of `anatomy`, `behavior`, `history`, `breeds`, `genetics`, `records`, `culture`, `science`. |
| `source_title` | The title of the outside source, as the article cites it. |
| `source_url` | The outside source for this fact: a study, registry, museum, newspaper, reference book or similar. It is never a cattriviagames.com page. |
| `article_url` | The Cat Trivia Games article that states the fact and cites the source. |
| `added` | The date the fact was added, as `YYYY-MM-DD`. |

Example:

```json
{
  "id": "kittens-open-eyes-days-old",
  "fact": "Kittens open their eyes when they are about 8 to 12 days old.",
  "category": "anatomy",
  "source_title": "How do cats see the world? What to know about cat vision",
  "source_url": "https://www.petmd.com/cat/general-health/cat-vision",
  "article_url": "https://cattriviagames.com/facts/cat-facts-for-kids",
  "added": "2026-11-02"
}
```

## Use it without hosting anything

jsDelivr serves files from public GitHub repositories through its CDN, so you can load the data straight from there:

```
https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.json
https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.csv
```

Please use these URLs (or your own copy of the files) rather than requesting pages from cattriviagames.com. The `@main` address follows the latest version, and the CDN can take a while to pick up a change. To stay on one exact version, replace `@main` with a release tag or a commit hash.

In a web page or in Node 18 or newer:

```js
const url = "https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.json";
const facts = await (await fetch(url)).json();
const pick = facts[Math.floor(Math.random() * facts.length)];
console.log(pick.fact);
console.log("Cat facts from Cat Trivia Games, https://cattriviagames.com, CC BY 4.0");
```

In Python 3:

```python
import json, random, urllib.request

url = "https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.json"
with urllib.request.urlopen(url) as response:
    facts = json.load(response)
pick = random.choice(facts)
print(pick["fact"])
print("Cat facts from Cat Trivia Games, https://cattriviagames.com, CC BY 4.0")
```

The scripts in `examples/` do the same, take an optional category, and can read a local copy of `facts.json`:

```
node examples/random-fact.js --category history
python3 examples/random_fact.py --category genetics
python3 examples/random_fact.py --file facts.json
```

## License and credit

The facts and the files in this repository are released under the [Creative Commons Attribution 4.0 International license (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may copy, share, adapt and use them, including commercially, as long as you give credit.

Use this credit line wherever the facts appear, in a place your readers or users can see it:

> Cat facts from Cat Trivia Games, https://cattriviagames.com, CC BY 4.0

On a web page you can link it:

```html
<p>Cat facts from <a href="https://cattriviagames.com">Cat Trivia Games</a>, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></p>
```

If you change a fact's wording, say that you changed it. The license covers the wording of these facts. The outside sources keep their own copyright and terms; this dataset links to them and does not copy them.

## How the facts are sourced

Every fact was written from an article published on cattriviagames.com in the `facts`, `behavior` or `science` sections. A fact is only included when the article states it and cites an outside source for it, and `source_url` is that source. The wording of each fact was then checked against the source itself, by fetching the cited page or paper (for a few journal papers, the published abstract) and reading the passage that supports it. Where a source supported only a narrower claim, the fact was rewritten to match the source, and facts that could not be confirmed were left out. The quiz and trivia question bank used by the Cat Trivia Games app is not part of this dataset.

Some facts describe a single study or a registry rule. Read them as what that source reports, not as a rule for every cat. Nothing here is veterinary advice: if your cat seems unwell, ask a veterinarian.

How articles are written and corrected is explained in the site's [editorial policy](https://cattriviagames.com/about/editorial-policy).

## Corrections

If a fact is wrong, out of date or does not match its source, open an issue in this repository with the fact's `id` and what the source says. Corrections change the `fact` text, and sometimes the source, but keep the same `id`. A fact that cannot be fixed is removed.

To make a change yourself, edit `facts.json`, run `python3 build_dataset.py`, and commit all three changed files (`facts.json`, `facts.csv` and `README.md`). `python3 build_dataset.py --check` validates the data and reports any file that is out of date, which is useful in continuous integration.

## Play with the facts

Cat Trivia Games has free cat trivia in the browser, with no account needed:

- [Daily cat trivia](https://cattriviagames.com/daily): five new questions every day, with explanations.
- [Cat Trivia Battle](https://cattriviagames.com/battle): play live against friends, family or the computer.
- [The Cat Museum](https://cattriviagames.com/museum): browse public domain cat artworks from five museums, then play a game.
