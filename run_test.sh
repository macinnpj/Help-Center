#!/bin/bash
# Runs each test question through gnosis-mcp in keyword mode and hybrid mode.
# Output is printed and saved to output.txt.

: > output.txt
while IFS='|' read -r question expected; do
  [ -z "$question" ] && continue
  {
    echo "=================================================="
    echo "QUESTION: $question"
    echo "SHOULD FIND: $expected"
    echo "--- Keyword search ---"
    gnosis-mcp search "$question"
    echo "--- Hybrid search (keyword + meaning) ---"
    gnosis-mcp search "$question" --embed
    echo
  } 2>&1 | tee -a output.txt
done < questions.txt

echo "Done. Results saved to output.txt"
