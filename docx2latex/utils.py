from __future__ import annotations

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def read_text_file(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def sanitize_latex(value: str) -> str:
    return value.replace('&', '\\&').replace('%', '\\%')
