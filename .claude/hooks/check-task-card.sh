#!/usr/bin/env bash
# Энфорсмент ADR-0006: карточка задачи не регистрируется без тикета и без
# предъявимого артефакта. PreToolUse Write на 10-governance/tasks/*.md.
# Гейт на РЕГИСТРАЦИЮ (создание = Write с полным содержимым); правки (Edit) пропускаем.

input=$(cat)
path=$(printf '%s' "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
[ -z "$path" ] && exit 0
rel=${path#"$CLAUDE_PROJECT_DIR"/}

case "$rel" in
  10-governance/tasks/*.md) ;;
  *) exit 0 ;;
esac

# полное содержимое есть только у Write; у Edit/MultiEdit его нет — гейт на создание
content=$(printf '%s' "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('content',''))" 2>/dev/null)
[ -z "$content" ] && exit 0

printf '%s' "$content" | python3 "$CLAUDE_PROJECT_DIR/80-kernel/scripts/task-card-check.py"
exit $?
