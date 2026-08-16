#!/usr/bin/env python3
import pathlib
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: apply-about-card-fix.py <recovery-root>")

root = pathlib.Path(sys.argv[1])
files = (
    "gui/theme/portrait_hdpi/themes/style.xml",
    "gui/theme/portrait_hdpi/themes/styles/Black.xml",
    "gui/theme/portrait_hdpi/themes/styles/Cream.xml",
    "gui/theme/portrait_hdpi/themes/styles/Dark.xml",
    "gui/theme/portrait_hdpi/themes/styles/Gray.xml",
    "gui/theme/portrait_hdpi/themes/styles/Light.xml",
)
old = b'filename="SVG/About/card.svg" retainaspect="1"'
new = b'filename="SVG/About/card.svg"'

for relative in files:
    path = root / relative
    data = path.read_bytes()
    count = data.count(old)
    if count != 1:
        raise SystemExit(f"{relative}: expected exactly one About card match, found {count}")
    updated = data.replace(old, new)
    if updated.count(old) != 0 or updated.count(new) != 1:
        raise SystemExit(f"{relative}: About card replacement verification failed")
    path.write_bytes(updated)
    print(f"fixed {relative}")