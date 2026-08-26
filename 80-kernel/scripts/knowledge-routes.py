#!/usr/bin/env python3
"""Маршрутизатор знания: по пути правки называет файлы 30-knowledge, объявившие этот путь своим.

Маршрут объявляет сам файл знания — ключом `routes:` во frontmatter. Хук списка
не носит: иначе машинерия начнёт нести данные и разойдётся с содержимым слоя.

Гейт срабатывает один раз на файл знания за сессию: повтор того же вызова
проходит. Смысл в моменте, а не в частоте — первая правка в классе работы есть
единственная точка, где чтение ещё дешевле переделки.
"""

import fnmatch
import json
import os
import re
import sys
from pathlib import Path

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
# routes: [a, b] либо блок «- a» построчно
ROUTES_INLINE = re.compile(r"^routes:\s*\[(.*?)\]\s*$", re.MULTILINE)
ROUTES_BLOCK = re.compile(r"^routes:\s*\n((?:\s*-\s*.+\n?)+)", re.MULTILINE)


def declared_routes(text):
    fm = FRONTMATTER.match(text)
    if not fm:
        return []
    head = fm.group(1)
    inline = ROUTES_INLINE.search(head)
    if inline:
        return [p.strip().strip("\"'") for p in inline.group(1).split(",") if p.strip()]
    block = ROUTES_BLOCK.search(head)
    if block:
        return [
            line.strip().lstrip("-").strip().strip("\"'")
            for line in block.group(1).splitlines()
            if line.strip()
        ]
    return []


def main():
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project:
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_input = payload.get("tool_input", {})
    root = Path(project).resolve()

    def relativise(raw):
        raw = raw.strip().strip("\"'")
        if not raw or "/" not in raw:
            return None
        try:
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = root / raw
            return str(candidate.resolve().relative_to(root))
        except (ValueError, OSError):
            return None

    # Write/Edit несут путь полем; bash-режим этой установки правит файлы через sed и
    # heredoc, поэтому команда разбирается на путеподобные токены — иначе гейт сторожил бы
    # путь, которым здесь почти не ходят.
    candidates = []
    if tool_input.get("file_path"):
        candidates.append(tool_input["file_path"])
    for token in re.split(r"[\s;|&<>()]+", tool_input.get("command", "")):
        candidates.append(token)

    rels = {r for r in (relativise(c) for c in candidates) if r}
    # правка самого знания маршрутизации не требует
    rels = {r for r in rels if not r.startswith("30-knowledge/")}
    if not rels:
        return 0

    knowledge = Path(project) / "30-knowledge"
    if not knowledge.is_dir():
        return 0

    # session_id даёт область жизни штампа; без него деградируем до суток,
    # иначе гейт молча превратился бы в вечный
    scope = payload.get("session_id") or f"day-{__import__('time').strftime('%Y%m%d')}"
    stamps = Path(os.environ.get("TMPDIR", "/tmp")) / "adversaria-knowledge-router" / scope

    matched = []
    for note in sorted(knowledge.glob("*.md")):
        try:
            text = note.read_text(encoding="utf-8")
        except OSError:
            continue
        # fnmatch: '*' пересекает разделитель каталогов, поэтому `.repos*/kub/helm-charts/*`
        # достаёт и рабочее дерево, и любую глубину внутри чарта
        patterns = declared_routes(text)
        # Каталог тоже есть контакт с классом: `git -C .repos/kub/argocd` не совпадает
        # с глобом `.repos/kub/argocd/*`, но маршрут лежит под ним.
        hits = sorted(
            rel
            for rel in rels
            for p in patterns
            if fnmatch.fnmatch(rel, p) or p.startswith(rel.rstrip("/") + "/")
        )
        if hits and not (stamps / note.name).exists():
            matched.append((note, hits[0]))

    if not matched:
        return 0

    stamps.mkdir(parents=True, exist_ok=True)
    for note, _ in matched:
        (stamps / note.name).touch()

    # путь называется рядом с файлом: иначе гейт сообщает про один путь, а файл
    # сопоставлен другим, и сообщение читается как ошибка маршрута
    listing = "\n".join(f"  30-knowledge/{note.name}  ← {hit}" for note, hit in matched)
    print(
        "Работа попадает в класс, о котором в vault уже есть запись:\n"
        f"{listing}\n"
        "Прочитай её и повтори вызов — второй раз гейт пропустит. "
        "Там методы, замеры и опровергнутые гипотезы, которые дешевле прочитать, чем нажить.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
