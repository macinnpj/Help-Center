"""Standard BM25 keyword ranking with punctuation stripping, light stemming,
and English stopword removal. Written for comparison only: this approximates the
keyword half of hybrid tools such as gnosis-mcp. It is not gnosis-mcp and has
no semantic (embedding) search.
"""
import math
import pathlib
import re
import sys

corpus = pathlib.Path(sys.argv[1])
docs = {p.stem: p.read_text(encoding="utf-8") for p in sorted(corpus.glob("*.md"))}

STOP = set("a an and are as at be by can can't do does for from how i in is it my of on or the to what with you your".split())


def stem(w):
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def toks(text):
    words = re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())
    return [stem(w) for w in words if w not in STOP]


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

tok = {d: toks(t) for d, t in docs.items()}
N = len(tok)
avg = sum(len(v) for v in tok.values()) / N
k1, b = 1.5, 0.75


def bm25(d, q):
    s = 0.0
    for t in q:
        n = sum(1 for v in tok.values() if t in v)
        if n == 0:
            continue
        idf = math.log(1 + (N - n + 0.5) / (n + 0.5))
        f = tok[d].count(t)
        s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(tok[d]) / avg))
    return s


hits = 0
for query, expected in TESTS:
    q = toks(query)
    ranked = sorted(docs, key=lambda d: (-bm25(d, q), d))
    top = ranked[0] if bm25(ranked[0], q) > 0 else "(no match)"
    ok = top == expected
    hits += ok
    print(f"{'PASS' if ok else 'FAIL'}  {query!r:34} terms={q}  top-1: {top}")
print(f"\nTop-1 accuracy: {hits}/{len(TESTS)}")
