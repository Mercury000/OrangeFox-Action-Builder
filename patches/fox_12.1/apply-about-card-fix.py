#!/usr/bin/env python3
import pathlib
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: apply-about-card-fix.py <recovery-root>")

root = pathlib.Path(sys.argv[1])
style_files = (
    "gui/theme/portrait_hdpi/themes/style.xml",
    "gui/theme/portrait_hdpi/themes/styles/Black.xml",
    "gui/theme/portrait_hdpi/themes/styles/Cream.xml",
    "gui/theme/portrait_hdpi/themes/styles/Dark.xml",
    "gui/theme/portrait_hdpi/themes/styles/Gray.xml",
    "gui/theme/portrait_hdpi/themes/styles/Light.xml",
)

for relative in style_files:
    path = root / relative
    data = path.read_bytes()
    old = b'filename="SVG/About/card.svg" retainaspect="1"'
    new = b'filename="SVG/About/card.svg"'
    if data.count(old) == 1:
        updated = data.replace(old, new)
    elif data.count(old) == 0 and data.count(new) == 1:
        updated = data
    else:
        raise SystemExit(f"{relative}: expected one unfixed or one fixed About card match")
    if updated.count(old) != 0 or updated.count(new) != 1:
        raise SystemExit(f"{relative}: About card replacement verification failed")
    path.write_bytes(updated)
    print(f"fixed {relative}")

card = root / "gui/theme/portrait_hdpi/images/SVG/About/card.svg"
card_data = card.read_bytes()
if b"M 168,72" in card_data:
    raise SystemExit("card.svg still contains the avatar cutout path")
if card_data.count(b"<path") != 1:
    raise SystemExit("card.svg must contain exactly one outer card path")

settings = (root / "gui/theme/portrait_hdpi/pages/settings.xml").read_text(encoding="utf-8")
search_from = 0
for resource in ("author_yan", "author_fd", "author_jabba", "maintainer_img"):
    card_pos = settings.find('<image resource="card"', search_from)
    image_pos = settings.find(f'<image resource="{resource}"', search_from)
    if card_pos < 0 or image_pos < 0 or card_pos > image_pos:
        raise SystemExit(f"settings.xml: card must be drawn before {resource}")
    search_from = image_pos + 1

print("validated About card geometry and draw order")
