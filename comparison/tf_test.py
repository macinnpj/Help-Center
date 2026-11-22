"""Reimplementation of Context Engine v0 selection (context-core TermFrequencyScorer).

Score = occurrences of any query term among the document's lowercased,
whitespace-split words, divided by total words. No stemming, no stopword
removal, no punctuation stripping. Ties break by document id ascending.
Tokens = ceil(len(content) / 4). Docs are taken in rank order while they fit the budget.
"""
import pathlib
import sys

corpus = pathlib.Path(sys.argv[1])
budget = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
docs = {p.stem: p.read_text(encoding="utf-8") for p in sorted(corpus.glob("*.md"))}

TESTS = [
    ("can't sign in", "creating-an-account"),
    ("log in", "creating-an-account"),
    ("make my resume private", "resume-builder"),
    ("can employers see my profile", "profile-settings-privacy"),
    ("passkey", "whats-new"),
    ("change my job preferences", "profile-preferences"),
    ("upload resume", "resume-builder"),
    ("hcaptcha", "creating-an-account"),
]


def score(text, query):
    words = text.lower().split()
    terms = query.lower().split()
    if not words or not terms:
        return 0.0, 0, len(words)
    matches = sum(1 for w in words for t in terms if w == t)
    return matches / len(words), matches, len(words)


hits = 0
for query, expected in TESTS:
    ranked = sorted(docs, key=lambda d: (-score(docs[d], query)[0], d))
    selected, used = [], 0
    for d in ranked:
        tokens = (len(docs[d]) + 3) // 4
        if used + tokens <= budget:
            selected.append(d)
            used += tokens
    top = ranked[0]
    ok = top == expected
    hits += ok
    print(f"\nQUERY: {query!r}  expected: {expected}  top-1: {top}  {'PASS' if ok else 'FAIL'}")
    for d in ranked:
        s, m, n = score(docs[d], query)
        flag = "selected" if d in selected else "cut by budget"
        print(f"  {s:.4f}  matches={m:<3} words={n:<4} {d}  [{flag}]")
print(f"\nTop-1 accuracy: {hits}/{len(TESTS)} (budget {budget} tokens)")
