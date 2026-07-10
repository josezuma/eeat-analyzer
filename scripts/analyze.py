#!/usr/bin/env python3
"""EEAT Analyzer — Score any URL for Experience, Expertise, Authoritativeness, Trustworthiness signals."""

import sys, re, json, argparse
from html.parser import HTMLParser


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.author = None
        self.schemas = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta" and d.get("name") == "author":
            self.author = d.get("content")


def score_eeat(url):
    score = 0
    findings = []

    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "EEAT-Analyzer/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"score": 0, "error": str(e), "findings": [f"Failed to fetch: {e}"]}

    # 1. Named author (25 pts)
    author_patterns = [
        r"by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
        '"author":\\s*"',
        '<meta\\s+name="author"',
    ]
    found_author = False
    for pat in author_patterns:
        if re.search(pat, html, re.I):
            score += 25
            findings.append("Named author found (+25)")
            found_author = True
            break
    if not found_author:
        findings.append("No named author (-25)")

    # 2. Publish date (20 pts)
    if re.search(r"\d{4}-\d{2}-\d{2}", html):
        score += 20
        findings.append("Publish date found (+20)")
    else:
        findings.append("No publish date detected")

    # 3. External references (20 pts)
    refs = re.findall(r'href="https?://([^"]+)"', html)
    domain = url.split("/")[2] if "//" in url else ""
    external = [r for r in refs if domain not in r]
    if len(external) >= 3:
        score += 20
        findings.append(f"{len(external)} external references (+20)")
    elif external:
        score += 10
        findings.append(f"{len(external)} external references (+10)")
    else:
        findings.append("No external references")

    # 4. Schema.org (20 pts)
    if re.search(r'"@type"\\s*:', html, re.I) or re.search(r'application/ld+json', html):
        score += 20
        findings.append("Schema.org markup found (+20)")
    else:
        findings.append("No schema.org markup")

    # 5. Credentials / social (15 pts)
    if re.search(r"(linkedin\.com/in/|twitter\.com/|github\.com/)", html, re.I):
        score += 15
        findings.append("Social/credential profiles found (+15)")
    else:
        findings.append("No social/credential profiles")

    return {"score": min(score, 100), "findings": findings, "url": url}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EEAT Analyzer")
    parser.add_argument("url", help="URL to analyze")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = score_eeat(args.url)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\nEEAT Score: {result['score']}/100 for {args.url}\n")
        for f in result.get("findings", []):
            print(f"  {f}")
        print()

    with open("eeat-result.json", "w") as f:
        json.dump(result, f, indent=2)
