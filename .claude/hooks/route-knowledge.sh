#!/usr/bin/env bash
# Маршрутизатор знания (ADR-0016). PreToolUse на Write|Edit|MultiEdit:
# если путь правки объявлен во frontmatter файла 30-knowledge ключом `routes:`,
# гейт называет этот файл и пропускает повторный вызов.
# Список маршрутов живёт в самом знании, а не здесь.

exec python3 "$CLAUDE_PROJECT_DIR/80-kernel/scripts/knowledge-routes.py"
