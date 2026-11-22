# Results: help center search test

Earlier results came from reproductions run by Claude, not the tools themselves. The gnosis-mcp columns come from a real run on November 22, 2026 (SQLite backend, local embedding model MongoDB/mdbr-leaf-ir). Full output: [results/output.txt](results/output.txt).

| Question | Should find | Context Engine (exact words) | Keyword search (BM25) | gnosis keyword | gnosis hybrid |
|---|---|---|---|---|---|
| can't sign in | creating-an-account | Pass | Pass | Pass | Pass |
| log in | creating-an-account | Fail | Fail (no match) | Fail (top: profile-settings-privacy) | Fail (top: profile-preferences) |
| make my resume private | resume-builder | Pass | Fail (pre-2022 article first) | Fail (pre-2022 article first) | Fail (pre-2022 article first) |
| can employers see my profile | profile-settings-privacy | Pass | Pass | Fail (pre-2022 article first) | Fail (pre-2022 article first) |
| passkey | whats-new | Fail | Pass | Pass | Pass |
| change my job preferences | profile-preferences | Pass | Pass | Pass | Pass |
| upload resume | resume-builder | Pass | Pass | Pass | Pass |
| hcaptcha | creating-an-account | Pass | Pass | Pass | Pass |
| **Total** | | **6 of 8** | **6 of 8** | **5 of 8** | **5 of 8** |

## Notes

- **Hybrid search scored the same as keyword search.** Both gnosis modes passed 5 of 8 questions and failed the same 3. In 7 of 8 questions, both modes returned the same top article. On "log in," the top articles differed, and both were wrong.
- **"log in" still fails.** The articles say "sign in." Keyword search matched only the word "in," and every result scored 0.0. Meaning-based search didn't connect "log in" with "sign in" either: creating-an-account ranked 3rd in both modes, behind "More in this topic" link lists.
- **The outdated pre-2022 article won both privacy questions.** what-employers-see-pre2022 ranked first for "make my resume private" and "can employers see my profile" in both modes. In hybrid mode, resume-builder ranked 3rd for the first question, and profile-settings-privacy ranked 3rd for the second. No search mode can tell which article is current. Retiring or redirecting the old article is the content fix.
- **"can employers see my profile" differs from the earlier BM25 result.** The earlier reproduction scored it a Pass. gnosis keyword search ranked the pre-2022 article first. This run doesn't show why the two differ; the earlier result came from a reproduction, not the original tool.
- **"upload resume" was a tie in hybrid mode.** resume-builder and profile-preferences both scored 0.0325, and resume-builder was listed first.
- **Navigation sections show up as results.** "More in this topic" and "Related articles" sections appear in the results for several questions. For "log in," these link lists ranked first in both modes. Excluding these sections from the index is worth testing.
