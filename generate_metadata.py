#!/usr/bin/env python3
"""Generate YouTube music channel metadata from background images."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


@dataclass(frozen=True)
class Theme:
    name: str
    name_kr: str
    seo_keywords: list[str]
    mood: str
    hook_lines: tuple[str, str]
    tags: list[str]


THEMES: dict[str, Theme] = {
    "FOCUS": Theme(
        name="FOCUS",
        name_kr="집중",
        seo_keywords=["lofi", "study", "focus", "work", "deep concentration"],
        mood="잔잔한 집중 모드",
        hook_lines=(
            "지금 바로 집중력을 끌어올리는 로파이 사운드를 시작하세요.",
            "잡음을 덜어내고 깊게 몰입할 시간입니다.",
        ),
        tags=[
            "lofi",
            "study music",
            "focus music",
            "deep focus",
            "work music",
            "productivity",
            "background music",
            "instrumental",
            "beats",
            "ambient",
            "chill",
            "카페 음악",
            "집중",
            "공부 음악",
            "작업 음악",
            "no vocals",
            "playlist",
            "relax",
            "coding music",
            "study playlist",
            "힐링",
            "quiet",
            "mindset",
        ],
    ),
    "SLEEP": Theme(
        name="SLEEP",
        name_kr="수면",
        seo_keywords=["sleep", "relax", "calm", "ambient", "night"],
        mood="포근한 밤의 휴식",
        hook_lines=(
            "눈을 감고 편안한 수면 사운드에 몸을 맡겨보세요.",
            "하루의 긴장을 녹여주는 부드러운 멜로디가 이어집니다.",
        ),
        tags=[
            "sleep music",
            "relax",
            "calm",
            "ambient",
            "night",
            "deep sleep",
            "soothing",
            "healing",
            "white noise",
            "sleep playlist",
            "no vocals",
            "meditation",
            "수면",
            "힐링",
            "휴식",
            "잔잔한 음악",
            "instrumental",
            "lofi",
            "quiet",
            "peaceful",
            "stress relief",
            "chill",
            "background music",
        ],
    ),
    "DRIVE": Theme(
        name="DRIVE",
        name_kr="드라이브",
        seo_keywords=["drive", "road", "cruise", "city night", "playlist"],
        mood="도시 야경과 달리는 템포",
        hook_lines=(
            "창밖으로 흐르는 야경과 함께 드라이브 감성을 채워보세요.",
            "속도를 올려도 마음은 여유로워지는 플레이리스트입니다.",
        ),
        tags=[
            "drive music",
            "road trip",
            "cruise",
            "city night",
            "playlist",
            "chill",
            "lofi",
            "synth",
            "night drive",
            "instrumental",
            "background music",
            "감성",
            "드라이브",
            "여행 음악",
            "기분 전환",
            "no vocals",
            "beats",
            "urban",
            "retro",
            "sunset",
            "energy",
            "relax",
            "mix",
        ],
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate metadata text files for YouTube music channels.",
    )
    parser.add_argument(
        "--input-dir",
        default="input/background",
        help="Directory containing background images.",
    )
    parser.add_argument(
        "--output-dir",
        default="output/metadata",
        help="Directory to write metadata files.",
    )
    parser.add_argument(
        "--theme",
        choices=sorted(THEMES.keys()),
        help="Force a theme for all outputs (FOCUS, SLEEP, DRIVE).",
    )
    return parser.parse_args()


def detect_theme(filename: str, forced_theme: str | None) -> Theme:
    if forced_theme:
        return THEMES[forced_theme]

    lower_name = filename.lower()
    if "sleep" in lower_name or "night" in lower_name:
        return THEMES["SLEEP"]
    if "drive" in lower_name or "road" in lower_name:
        return THEMES["DRIVE"]
    if "focus" in lower_name or "study" in lower_name or "work" in lower_name:
        return THEMES["FOCUS"]
    return THEMES["FOCUS"]


def build_titles(base_name: str, theme: Theme) -> list[str]:
    seo_title = (
        f"{base_name} | {theme.name_kr} {', '.join(theme.seo_keywords[:3])} 플레이리스트"
    )
    emotional_title = f"{theme.name_kr}을 위한 {theme.mood} – {base_name}"
    mix_title = (
        f"{base_name} {theme.name_kr} 믹스 | {theme.seo_keywords[0].upper()} & "
        f"{theme.seo_keywords[1].upper()}"
    )
    return [seo_title, emotional_title, mix_title]


def build_description(base_name: str, theme: Theme) -> str:
    lines = list(theme.hook_lines)
    lines.extend(
        [
            f"오늘의 무드는 '{base_name}' 입니다.",
            f"{theme.name_kr}에 어울리는 사운드로 흐름을 이어가 보세요.",
            "헤드폰/스피커 어느 쪽에서도 듣기 좋게 밸런스를 맞췄습니다.",
            "영상이 마음에 들었다면 좋아요와 구독으로 응원 부탁드려요.",
        ]
    )
    return "\n".join(lines)


def build_tags(base_name: str, theme: Theme) -> list[str]:
    tags = [base_name]
    tags.extend(theme.tags)
    unique = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    return unique[:30]


def build_pinned_comment(theme: Theme) -> str:
    return (
        "📌 고정댓글\n"
        f"오늘의 {theme.name_kr} 무드는 마음에 드셨나요?\n"
        "👉 더 많은 플레이리스트는 채널 홈에서 확인하세요!\n"
        "💬 어떤 상황에서 들으면 좋을지 댓글로 알려주세요.\n"
        "❤️ 구독과 좋아요는 큰 힘이 됩니다."
    )


def format_metadata(base_name: str, theme: Theme) -> str:
    titles = build_titles(base_name, theme)
    description = build_description(base_name, theme)
    tags = build_tags(base_name, theme)
    pinned_comment = build_pinned_comment(theme)

    sections = [
        "[제목 3안]",
        f"1) SEO: {titles[0]}",
        f"2) 감성: {titles[1]}",
        f"3) 믹스: {titles[2]}",
        "",
        "[설명]",
        description,
        "",
        "[태그]",
        ", ".join(tags),
        "",
        "[고정댓글]",
        pinned_comment,
        "",
    ]
    return "\n".join(sections)


def find_images(input_dir: Path) -> Iterable[Path]:
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    images = list(find_images(input_dir))
    if not images:
        raise SystemExit(f"No images found in {input_dir}")

    for image in images:
        theme = detect_theme(image.stem, args.theme)
        metadata = format_metadata(image.stem, theme)
        output_path = output_dir / f"{image.stem}_metadata.txt"
        output_path.write_text(metadata, encoding="utf-8")

    print(f"Generated metadata for {len(images)} file(s) in {output_dir}.")


if __name__ == "__main__":
    main()
