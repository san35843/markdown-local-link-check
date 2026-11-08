"""Check local inline Markdown links without making network requests."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"!?\[[^]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")


def check(root):
    root = Path(root).resolve()
    issues = []
    count = 0
    for document in sorted(root.rglob("*.md")):
        if any(part in {".git", "node_modules", ".venv"} for part in document.relative_to(root).parts):
            continue
        fenced = False
        fence_char = ""
        fence_length = 0
        for number, line in enumerate(document.read_text(encoding="utf-8-sig").splitlines(), 1):
            fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if fence:
                token = fence.group(1)
                if not fenced:
                    fenced, fence_char, fence_length = True, token[0], len(token)
                elif token[0] == fence_char and len(token) >= fence_length and not line[fence.end():].strip():
                    fenced = False
                continue
            if fenced:
                continue
            # Ignore simple single-backtick inline code spans.
            line = re.sub(r"`[^`]*`", "", line)
            for match in LINK.finditer(line):
                target = match.group(1).strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                count += 1
                relative = unquote(parsed.path)
                destination = root / relative.lstrip("/") if relative.startswith("/") else document.parent / relative
                if not destination.exists():
                    issues.append({"file": document.relative_to(root).as_posix(), "line": number, "target": target})
    return {"checked_links": count, "broken_links": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    if not Path(args.root).is_dir():
        parser.error("root must be a directory")
    try:
        result = check(args.root)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["broken_links"] else 0


if __name__ == "__main__":
    sys.exit(main())
