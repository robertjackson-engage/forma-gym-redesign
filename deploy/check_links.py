#!/usr/bin/env python3
"""
Link + asset integrity sweep over the built site (docs/).

Validates every internal href/src on every page against the filesystem, so a
broken link is caught before cutover rather than by a visitor.

  - /about/                -> docs/about/index.html
  - /assets/css/main.css?v -> docs/assets/css/main.css   (query stripped)
  - #fragments             -> checked for an id/name on the target page
  - http(s):, tel:, mailto:, data: -> skipped (external)

Exit code 1 if anything is broken, so it can gate a deploy.
"""
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")

ATTR = re.compile(r'(?:href|src)="([^"]+)"')
ID_ATTR = re.compile(r'(?:id|name)="([^"]+)"')
SKIP = re.compile(r"^(https?:|tel:|mailto:|data:|javascript:|//|#$)")


def page_files():
    for root, _dirs, files in os.walk(DOCS):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(root, fn)


def rel(p):
    return os.path.relpath(p, DOCS)


def resolve(url):
    """Map a site-absolute URL to an expected filesystem path (or None)."""
    path = url.split("#")[0].split("?")[0]
    if path == "":
        return None
    if not path.startswith("/"):
        return "RELATIVE"
    fs = os.path.join(DOCS, path.lstrip("/"))
    if path.endswith("/") or "." not in os.path.basename(path):
        return os.path.join(fs, "index.html")
    return fs


def main():
    broken = defaultdict(list)
    relative = defaultdict(list)
    frag_missing = defaultdict(list)
    ids_cache = {}
    total_links = 0
    pages = sorted(page_files())

    for pf in pages:
        html = open(pf, encoding="utf-8").read()
        for url in ATTR.findall(html):
            if SKIP.match(url):
                continue
            total_links += 1
            target = resolve(url)
            if target is None:
                continue
            if target == "RELATIVE":
                # after the Option A change every internal link should be
                # root-absolute; a relative one will break at some depth
                relative[rel(pf)].append(url)
                continue
            if not os.path.exists(target):
                broken[rel(pf)].append(url)
                continue
            # fragment check — only for links into HTML pages
            if "#" in url and target.endswith(".html"):
                frag = url.split("#", 1)[1]
                if frag:
                    if target not in ids_cache:
                        t_html = open(target, encoding="utf-8").read()
                        ids_cache[target] = set(ID_ATTR.findall(t_html))
                    if frag not in ids_cache[target]:
                        frag_missing[rel(pf)].append(url)

    print(f"Pages scanned : {len(pages)}")
    print(f"Links checked : {total_links}")
    print(f"Broken targets: {sum(len(v) for v in broken.values())}")
    print(f"Relative links: {sum(len(v) for v in relative.values())}")
    print(f"Dead fragments: {sum(len(v) for v in frag_missing.values())}")

    def dump(title, d):
        if not d:
            return
        print(f"\n--- {title} ---")
        for pg in sorted(d):
            for u in sorted(set(d[pg])):
                print(f"  {pg}  ->  {u}")

    dump("BROKEN (target file missing)", broken)
    dump("RELATIVE (should be root-absolute)", relative)
    dump("DEAD FRAGMENTS (no matching id on target)", frag_missing)

    if broken or relative:
        print("\nFAIL")
        return 1
    print("\nPASS" + ("  (fragments above are warnings only)" if frag_missing else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
