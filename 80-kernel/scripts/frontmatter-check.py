#!/usr/bin/env python3
"""Frontmatter-гейт (pre-commit). Проверяет заметки vault:
  1) YAML-валидность frontmatter — ловит осколки правки (кавычки в кавычках, висячие
     двоеточия), которые Obsidian показывает как «invalid properties»;
  2) схему статусов по ADR-0007 — для родов, где статус определён перечнем. Прочие
     рода проверяются только на валидность: правил под них не выдумываем.

Вход: имена файлов аргументами. Только .md. Exit 0 — чисто; exit 1 — нарушения.
pyyaml приходит через pre-commit (language: python, additional_dependencies).
"""
import re
import sys

import yaml

CONTENT = ["later", "in-progress", "processed", "done"]

# type → допустимые status. Рода нет в карте → status не проверяется.
STATUS = {
    "task": ["in-progress", "blocked", "done", "later"],
    "project": ["active", "paused", "done"],
    "note": CONTENT,
    "draft": CONTENT,
    "knowledge": ["later", "in-progress", "processed"],
    "adr": ["proposed", "accepted", "withdrawn"],  # + superseded* (префикс)
}


def frontmatter(txt):
    """Содержимое YAML-блока между ведущими '---' и следующим '---' (или None)."""
    if not txt.startswith("---"):
        return None
    parts = re.split(r"(?m)^---\s*$", txt, maxsplit=2)
    return parts[1] if len(parts) >= 3 else None


def main():
    fails = []
    for path in sys.argv[1:]:
        if not path.endswith(".md"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                txt = f.read()
        except OSError:
            continue

        fm = frontmatter(txt)
        if fm is None:
            continue
        try:
            data = yaml.safe_load(fm) or {}
        except yaml.YAMLError as e:
            fails.append(f"{path}: невалидный YAML frontmatter — {str(e).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            continue

        type_, status = data.get("type"), data.get("status")
        if type_ is None or status is None:
            continue
        allowed = STATUS.get(type_)
        if allowed is None:                       # род без схемы — только валидность
            continue

        ok = status in allowed or (type_ == "adr" and str(status).startswith("superseded"))
        if not ok:
            hint = ", ".join(allowed) + (", superseded*" if type_ == "adr" else "")
            fails.append(
                f"{path}: status '{status}' недопустим для type '{type_}' (ADR-0007). Допустимо: {hint}"
            )

    if fails:
        sys.stderr.write("✗ Frontmatter-гейт (ADR-0007) — коммит отклонён:\n")
        for f in fails:
            sys.stderr.write(f"  {f}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
