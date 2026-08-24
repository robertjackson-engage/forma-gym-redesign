#!/usr/bin/env python3
"""Generate responsive image variants into docs/assets/img/r/.

Run on macOS — it shells out to `sips`, which Linux CI does not have. That is
why the variants are committed: build.py only ever *reads* what is on disk and
falls back to the plain src when a variant is missing, so a CI build without
sips still produces a working site.

    python3 tools/gen_responsive.py          # incremental
    python3 tools/gen_responsive.py --force  # rebuild every variant
"""
import os, re, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs", "assets", "img")
OUT = os.path.join(IMG, "r")
WIDTHS = [400, 700, 1000, 1400]
QUALITY = "68"
# A few photos are almost entirely high-frequency detail — woven textiles, busy
# prints, wood grain edge to edge — and cost 3-5x a normal frame at QUALITY. The
# same texture also hides compression artefacts, so they can take a harder pass
# without looking worse. Keyed by filename so the choice travels with the photo.
BUSY = {
    "MB_LAB_1_1000px.jpg": "45",   # striped blanket + printed dress + wood floor
}
FORCE = "--force" in sys.argv


def dimensions(path):
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True, check=True).stdout
        w = int(re.search(r"pixelWidth:\s*(\d+)", out).group(1))
        h = int(re.search(r"pixelHeight:\s*(\d+)", out).group(1))
        return w, h
    except Exception:
        return None, None


def referenced():
    """Only bother with images the built site actually uses."""
    names = set()
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "*.html"), recursive=True):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        names |= set(re.findall(r"assets/img/([A-Za-z0-9._@%-]+\.(?:jpg|jpeg|png))", txt))
    return sorted(names)


def main():
    os.makedirs(OUT, exist_ok=True)
    made = skipped = 0
    saved_from = saved_to = 0
    for name in referenced():
        src = os.path.join(IMG, name)
        if not os.path.exists(src):
            continue
        w, _ = dimensions(src)
        if not w:
            continue
        stem, ext = os.path.splitext(name)
        for target in WIDTHS:
            # No point upscaling, and no point in a variant within 10% of the
            # original — it would not save enough to justify the extra file.
            if target >= w * 0.9:
                continue
            dst = os.path.join(OUT, f"{stem}-{target}{ext}")
            if not FORCE and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                skipped += 1
                continue
            quality = BUSY.get(os.path.basename(src), QUALITY)
            subprocess.run(["sips", "-Z", str(target), "--setProperty", "formatOptions",
                            quality, src, "--out", dst],
                           capture_output=True, check=False)
            if not os.path.exists(dst):
                continue
            # Some sources are already compressed harder than this pass, so a
            # smaller-pixel variant can come out *bigger*. Serving that would
            # make the page worse, so drop it and let the original stand.
            if os.path.getsize(dst) >= os.path.getsize(src):
                os.remove(dst)
                continue
            made += 1
            saved_from += os.path.getsize(src)
            saved_to += os.path.getsize(dst)
    print(f"variants written: {made}   up to date: {skipped}")
    if made:
        print(f"a {saved_from // 1024} KB set of sources became {saved_to // 1024} KB of variants")


if __name__ == "__main__":
    main()
