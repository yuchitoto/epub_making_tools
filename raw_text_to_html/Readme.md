# raw\_text\_to\_html.py
Takes text to be converted in text.txt. Use rules in rule.csv to specify the usual cases for tag adding.
If special cases are needed for the result, the code might be amended as specified in the code.

Produces content.txt which is a html tagged version of text.txt.

Each line in text.txt will be marked as a paragraph (p tag) in output.

| Specification ||
| --- | --- |
| Input: | text.txt (UTF8), rule.csv (UTF8) |
| Output: | content.txt (UTF8) |
| Version: | 1.0.1 |
