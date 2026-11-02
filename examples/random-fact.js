#!/usr/bin/env node
// Print a random cat fact with its source and the required credit line.
// Needs Node 18 or newer (for the built-in fetch). No packages to install.
//
//   node examples/random-fact.js
//   node examples/random-fact.js --category history
//   node examples/random-fact.js --file facts.json      (read a local copy instead of the CDN)

"use strict";

const DATA_URL = "https://cdn.jsdelivr.net/gh/cattriviagames/cat-facts-dataset@main/facts.json";
const CREDIT = "Cat facts from Cat Trivia Games, https://cattriviagames.com, CC BY 4.0";
const CATEGORIES = ["anatomy", "behavior", "history", "breeds", "genetics", "records", "culture", "science"];

function readArgs(argv) {
  const args = { category: null, file: null, url: DATA_URL };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--category" || a === "-c") args.category = (argv[++i] || "").toLowerCase();
    else if (a === "--file" || a === "-f") args.file = argv[++i];
    else if (a === "--url") args.url = argv[++i];
    else if (a === "--help" || a === "-h") args.help = true;
    else throw new Error(`Unknown option: ${a}`);
  }
  return args;
}

async function loadFacts(args) {
  if (args.file) {
    const fs = require("fs");
    return JSON.parse(fs.readFileSync(args.file, "utf8"));
  }
  const res = await fetch(args.url);
  if (!res.ok) throw new Error(`Could not load ${args.url} (HTTP ${res.status})`);
  return res.json();
}

function pickFact(facts, category) {
  const pool = category ? facts.filter((f) => f.category === category) : facts;
  if (pool.length === 0) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}

async function main() {
  const args = readArgs(process.argv.slice(2));
  if (args.help) {
    console.log("Usage: node random-fact.js [--category NAME] [--file facts.json] [--url URL]");
    console.log("Categories: " + CATEGORIES.join(", "));
    return;
  }
  if (args.category && !CATEGORIES.includes(args.category)) {
    throw new Error(`Unknown category "${args.category}". Use one of: ${CATEGORIES.join(", ")}`);
  }
  const facts = await loadFacts(args);
  const fact = pickFact(facts, args.category);
  if (!fact) throw new Error("No facts found.");
  console.log(fact.fact);
  console.log("");
  console.log(`Category: ${fact.category}`);
  console.log(`Source:   ${fact.source_title} <${fact.source_url}>`);
  console.log(`Article:  ${fact.article_url}`);
  console.log("");
  console.log(CREDIT);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
}

module.exports = { pickFact, CREDIT };
