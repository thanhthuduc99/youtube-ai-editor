"""Generate one thumbnail with Codex image_gen (the ChatGPT plan logged in to Codex CLI, no API key), feeding real
reference images. Prompt text lives in prompts/<name>.txt (built by build_prompts.py). Output: out/<name>.png (+ .log).
One run costs about 25-45k tokens of the Codex plan quota.

Usage (from the project folder):
  python thumbnail/scripts/gen_thumb.py t1 --face T5.png T1.png "my face.png" \\
      --asset "Claude app icon=assets/logos/claude.png" --asset "real timeline UI screenshot=assets/ui/timeline.png"

--face   identity photos of the presenter (names are looked up in HEADSHOTS).
--asset  "role=path" (path relative to thumbnail/): a real logo or UI screenshot that must appear as-is.

image_gen accepts at most 5 reference images. Extra assets are merged into one labeled reference sheet.
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
HEADSHOTS = Path(os.environ.get("THUMB_HEADSHOTS", ROOT / "faces"))
MAX_REFS = 5
ASSET_RULE = ("This is the REAL asset: reproduce it exactly, same shapes, colors and layout. "
              "Do not redraw, restyle, recolor or simplify it.")


def resolve(p, base):
    p = Path(p)
    return p if p.is_absolute() else (base / p)


def make_sheet(assets, out):
    """Grid of (label, path) on white, each cell labeled 'A) role'."""
    font = ImageFont.truetype("arial.ttf", 30)
    cell_w, cell_h, label_h = 760, 460, 50
    cols = 2 if len(assets) > 1 else 1
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * (cell_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(assets):
        x, y = (i % cols) * cell_w, (i // cols) * (cell_h + label_h)
        img = Image.open(path).convert("RGBA")
        img.thumbnail((cell_w - 40, cell_h - 20))
        sheet.paste(img, (x + (cell_w - img.width) // 2, y + label_h + (cell_h - img.height) // 2), img)
        draw.text((x + 20, y + 10), label, fill="black", font=font)
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--face", nargs="*", default=[])
    ap.add_argument("--asset", action="append", default=[])
    args = ap.parse_args()

    images, roles = [], []
    for f in args.face:
        images.append(resolve(f, HEADSHOTS))
        roles.append("identity reference photo of the man (not an edit target)")
    assets = [(role, resolve(path, ROOT)) for role, path in (a.split("=", 1) for a in args.asset)]
    for img in images + [p for _, p in assets]:
        if not img.exists():
            raise SystemExit(f"missing image: {img}")

    (ROOT / "out").mkdir(exist_ok=True)
    sheet = None
    if len(images) + len(assets) > MAX_REFS:
        keep = MAX_REFS - len(images) - 1
        if keep < 0:
            raise SystemExit("too many face photos, use at most 4 when assets are attached")
        merged = [(f"{chr(65 + i)}) {role}", p) for i, (role, p) in enumerate(assets[keep:])]
        sheet = ROOT / "out" / f"{args.name}-sheet.png"
        make_sheet(merged, sheet)
        assets = assets[:keep]
        sheet_role = ("reference sheet of real assets, each labeled: "
                      + "; ".join(label for label, _ in merged) + f". {ASSET_RULE} Do not copy the labels or the white sheet.")
    for role, path in assets:
        images.append(path)
        roles.append(f"{role}. {ASSET_RULE}")
    if sheet:
        images.append(sheet)
        roles.append(sheet_role)

    image_list = "\n".join(f"Image {i}: {r}" for i, r in enumerate(roles, 1)) or "No images are attached."
    prompt = (
        "Use the built-in image_gen tool to generate exactly ONE image.\n"
        f"Attached images, in order:\n{image_list}\n\n"
        "Use the text between <<< and >>> verbatim as the image prompt, and pass the attached images to image_gen as references.\n"
        f"After generating, copy the image to out/{args.name}.png. Do not modify any other file. Print the saved path.\n\n"
        f"<<<\n{(ROOT / 'prompts' / f'{args.name}.txt').read_text(encoding='utf-8').strip()}\n>>>\n"
    )

    cmd = [shutil.which("codex"), "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(ROOT)]
    for img in images:
        cmd += ["-i", str(img)]
    cmd.append("-")
    with open(ROOT / "out" / f"{args.name}.log", "w", encoding="utf-8") as log:
        r = subprocess.run(cmd, input=prompt, text=True, encoding="utf-8", stdout=log, stderr=subprocess.STDOUT)
    out = ROOT / "out" / f"{args.name}.png"
    print(f"exit={r.returncode} {'OK ' + str(out) if out.exists() else 'NO IMAGE, see log'}")


if __name__ == "__main__":
    main()
