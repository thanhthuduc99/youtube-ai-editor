"""Review sheet + upload files for thumbnails.

  python thumbnail/scripts/finalize.py t1 t2 t3          -> out/review.jpg (full size + phone size, for the approval stop)
  python thumbnail/scripts/finalize.py --pick t2          -> out/thumbnail-youtube.jpg (1280x720 JPG under 2 MB, YouTube limit)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "out"


def fit(im, w, h):
    """Centre-crop to 16:9 and resize."""
    r = w / h
    if im.width / im.height > r:
        nw = round(im.height * r); im = im.crop(((im.width - nw) // 2, 0, (im.width - nw) // 2 + nw, im.height))
    else:
        nh = round(im.width / r); im = im.crop((0, (im.height - nh) // 2, im.width, (im.height - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


args = sys.argv[1:]
if args[:1] == ["--pick"]:
    im = fit(Image.open(OUT / f"{args[1]}.png").convert("RGB"), 1280, 720)
    dst = OUT / "thumbnail-youtube.jpg"
    for q in (92, 88, 84, 80):
        im.save(dst, quality=q, optimize=True)
        if dst.stat().st_size < 2_000_000:
            break
    print(f"{dst} {dst.stat().st_size // 1024} KB")
else:
    font = ImageFont.truetype("arial.ttf", 26)
    W, H, w, h = 960, 540, 320, 180
    sheet = Image.new("RGB", (W + w + 30, len(args) * (H + 50)), "#111")
    d = ImageDraw.Draw(sheet)
    for k, name in enumerate(args):
        im = Image.open(OUT / f"{name}.png").convert("RGB")
        y = k * (H + 50)
        sheet.paste(fit(im, W, H), (0, y + 40)); sheet.paste(fit(im, w, h), (W + 30, y + 40))
        d.text((8, y + 6), name, fill="white", font=font); d.text((W + 30, y + 6), "cỡ điện thoại", fill="#aaa", font=font)
    sheet.save(OUT / "review.jpg", quality=88)
    print(OUT / "review.jpg")
