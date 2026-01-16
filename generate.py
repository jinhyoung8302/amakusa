from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input" / "background"
OUTPUT_DIR = PROJECT_DIR / "output"

# Fixed text content (3 lines)
TEXT_LINES = [
    "PLAYLIST",
    "LOW NOISE SESSION",
    "Celestria Nova",
]

# Fixed layout settings
CANVAS_SIZE = (1280, 720)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 160)
SHADOW_OFFSET = (2, 2)

# Font configuration (edit if you want a different font)
# Windows default fonts are in C:\Windows\Fonts
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SIZES = [84, 64, 44]
LETTER_SPACING = [6, 4, 2]  # Fixed tracking in px, per line
LINE_SPACING = 12  # Fixed line spacing in px

# Fixed placement (top-left origin)
TEXT_ANCHOR = (80, 110)

# A/B test variants
SIZE_VARIANTS = {
    "sz1": [84, 64, 44],  # current baseline
    "sz2": [92, 70, 48],
    "sz3": [76, 58, 40],
}
TRACKING_VARIANTS = {
    "tr1": [6, 4, 2],  # current baseline
    "tr2": [2, 1, 0],
}
SHADOW_VARIANTS = {
    "sh1": True,   # current baseline (shadow on)
    "sh0": False,  # shadow off
}


def load_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    if not Path(font_path).exists():
        raise FileNotFoundError(
            f"Font not found: {font_path}. Edit FONT_PATH in generate.py."
        )
    return ImageFont.truetype(font_path, size=size)


def open_background(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return image


def fit_to_canvas(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = image.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # Wider than target, crop sides
        new_h = src_h
        new_w = int(src_h * target_ratio)
    else:
        # Taller than target, crop top/bottom
        new_w = src_w
        new_h = int(src_w / target_ratio)

    left = (src_w - new_w) // 2
    top = (src_h - new_h) // 2
    cropped = image.crop((left, top, left + new_w, top + new_h))
    return cropped.resize((target_w, target_h), Image.LANCZOS)


def draw_text_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    start: tuple[int, int],
    color: tuple[int, int, int],
    tracking: int,
) -> None:
    x, y = start
    for ch in text:
        draw.text((x, y), ch, font=font, fill=color)
        bbox = font.getbbox(ch)
        ch_width = bbox[2] - bbox[0]
        x += ch_width + tracking


def draw_text_block(
    base: Image.Image,
    sizes: list[int],
    tracking_list: list[int],
    shadow_on: bool,
) -> None:
    draw = ImageDraw.Draw(base)
    x, y = TEXT_ANCHOR

    fonts = [load_font(FONT_PATH, size) for size in sizes]

    for line, font, tracking in zip(TEXT_LINES, fonts, tracking_list):
        if shadow_on:
            shadow_pos = (x + SHADOW_OFFSET[0], y + SHADOW_OFFSET[1])
            draw_text_line(draw, line, font, shadow_pos, SHADOW_COLOR, tracking)
        # Main text
        draw_text_line(draw, line, font, (x, y), TEXT_COLOR, tracking)

        line_height = font.getbbox("Hg")[3] - font.getbbox("Hg")[1]
        y += line_height + LINE_SPACING


def iter_backgrounds() -> Iterable[Path]:
    if not INPUT_DIR.exists():
        return []
    return [p for p in INPUT_DIR.iterdir() if p.is_file()]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    backgrounds = list(iter_backgrounds())

    if not backgrounds:
        print(f"No background images found in {INPUT_DIR}")
        return

    for bg_path in backgrounds:
        base = open_background(bg_path)
        for size_key, sizes in SIZE_VARIANTS.items():
            for track_key, tracking_list in TRACKING_VARIANTS.items():
                for shadow_key, shadow_on in SHADOW_VARIANTS.items():
                    canvas = fit_to_canvas(base, CANVAS_SIZE)
                    draw_text_block(canvas, sizes, tracking_list, shadow_on)

                    version = f"{size_key}_{track_key}_{shadow_key}"
                    out_name = f"{bg_path.stem}_{version}.png"
                    out_path = OUTPUT_DIR / out_name
                    canvas.save(out_path, format="PNG")
                    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
