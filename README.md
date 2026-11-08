# Markdown Local Link Check

Find broken local file links in Markdown documentation, entirely offline. A small Python tool with no third-party dependencies.

## Run

Requires Python 3.10+.

```sh
python mdlinks.py .
python -m unittest -v
```

JSON output includes checked link count and broken links with filename, line number and target. Exit codes: `0` no broken links, `1` broken links, `2` invalid input or read error.

Supports simple inline links and images, URL-encoded filenames, relative paths and repository-root paths starting with `/`. Query strings and fragments are removed before checking file existence. External URLs, anchor-only links, fenced code blocks and simple inline code spans are skipped. Ignores `.git`, `node_modules` and `.venv` directories.

## Scope and limitations

This is intentionally a lightweight scanner, not a full CommonMark parser. Reference-style links, complex nested parentheses, escaped brackets, HTML links and multi-backtick inline code are not supported. It does not validate heading anchors, external URLs, file case across different operating systems, or paths outside the repository boundary. Only lowercase `.md` files are scanned. Use it on trusted local repositories; filesystem links are resolved normally. No network requests are made and files are not modified.

## Contributing

Report a minimal Markdown example and expected result. Add a regression test for changes and run `python -m unittest -v`.

## Status

Initial release, created with AI assistance. No adoption claims. MIT licensed.
