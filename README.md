# Help Center Search Test Kit (gnosis-mcp)

This kit tests whether hybrid search (keyword plus meaning-based) finds the right help article for real user questions. It uses 6 of Jay's Indeed Help Center articles and the same 8 questions already run against two keyword-only methods.

Time: about 10 minutes. You need a Mac with Python 3.10 or later. Check by typing `python3 --version` in Terminal.

## What's in this folder

- `articles/`: the 6 help articles as Markdown files
- `questions.txt`: the 8 test questions and the article each one should find
- `run_test.sh`: runs all 8 questions in both modes and saves the output
- `results.md`: a table to fill in
- `comparison/`: the two scripts behind the earlier results, if you want to rerun them

## Steps

1. Unzip this folder and open Terminal in it. In Finder, right-click the folder, then choose New Terminal at Folder.

2. Create a private Python environment so nothing touches the rest of your Mac:

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install gnosis-mcp with local embeddings (no API key needed):

   ```
   pip install "gnosis-mcp[embeddings]"
   ```

4. Load the articles. The first command builds the keyword index. The second adds meaning-based search:

   ```
   gnosis-mcp ingest ./articles
   gnosis-mcp ingest ./articles --embed
   ```

5. Run the test:

   ```
   bash run_test.sh
   ```

   It prints results and saves them to `output.txt`.

6. For each question, look at the top result in both modes. Fill in `results.md`.

## If a command fails

The tool is updated often, so a flag may change. Type `gnosis-mcp --help` or `gnosis-mcp search --help` to see the current options, then adjust the command. If you get stuck, paste the error into Claude.

## What to look for

- **"log in":** the articles only say "sign in." Keyword search can't connect the two, so this is the real test of meaning-based search.
- **"make my resume private":** the outdated pre-2022 article ("What do Employers see") beat the current Resume Builder article in keyword search. Check whether hybrid search makes the same mistake. No search tool knows which article is current, which is why content quality review still matters.

## Cleanup

Delete the folder when you're done. Everything installed lives inside `.venv` in this folder. gnosis-mcp may also create a small database file. `gnosis-mcp --help` shows where it keeps it.
