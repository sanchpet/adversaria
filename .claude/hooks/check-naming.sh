#!/usr/bin/env bash
# Энфорсмент ADR-0003 (имена файлов). PreToolUse на Write|Edit|MultiEdit:
# блокирует создание или правку файла с пробелами, кириллицей или произвольным
# верхним регистром в имени. Разрешено: опциональный ЗАГЛАВНЫЙ инвентарный префикс
# (ADR-0007-, P3-) + строчная смысловая часть. Тикет в имени файла — строчный,
# каноническое написание живёт во frontmatter.
# Человекочитаемость — через aliases, не через имя файла.

input=$(cat)
path=$(printf '%s' "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
[ -z "$path" ] && exit 0

rel=${path#"$CLAUDE_PROJECT_DIR"/}

# dot-зона и сторонние конфиги — не наши имена, пропускаем
case "$rel" in
  .obsidian/*|.git/*|.repos/*|.repos-wip/*|.principles/*|.vscode/*) exit 0 ;;
esac

base=$(basename "$rel")

# tooling-токены — исключения ADR-0003
case "$base" in
  README.md|LICENSE|CLAUDE.md|MEMORY.md|SKILL.md) exit 0 ;;
esac

if ! printf '%s' "$base" | grep -qE '^([A-Z]+-?[0-9]+-)?[a-z0-9._-]+$'; then
  echo "ADR-0003: имя — строчная латиница без пробелов и кириллицы; допускается лишь ЗАГЛАВНЫЙ инвентарный префикс (ADR-0007-, P3-). Получено: '$base'. Человекочитаемое имя ставь в aliases." >&2
  exit 2
fi
exit 0
