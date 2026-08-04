#!/usr/bin/env bash
# Детектор ритма (INV-5 / INV-9 / INV-17 «система-как-код»).
# Носитель обещания «незакрытый день ДЕТЕКТИРУЕТСЯ»: запускается хуком SessionStart
# (каждый старт сессии) и шагом 0 в /open. Печатает флаги ТОЛЬКО при отклонениях —
# детект, а не блок. Тихо, когда всё закрыто.
set -euo pipefail

root=$(git -C "${CLAUDE_PROJECT_DIR:-$PWD}" rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" 2>/dev/null || exit 0

today=$(date +%Y-%m-%d)
flags=()
shopt -s nullglob

# 1. Незакрытый день: DayPlan прошлого дня остался в current/ (его архивирует /close).
for f in 10-governance/plans/current/dayplan-*.md; do
  d=$(basename "$f" | sed -E 's/dayplan-([0-9-]+)\.md/\1/')
  [ "$d" \< "$today" ] && flags+=("день $d не закрыт (DayPlan не в архиве) → /close")
done

# 2. Инбокс: записи старше недели — кандидаты в архив (strict-режим триажа).
# Порог согласован с 80-kernel/docs/inbox-triage.md; правится там же и здесь за один коммит.
stale=0
cutoff=$(date -v-7d +%s 2>/dev/null || date -d '7 days ago' +%s 2>/dev/null || echo 0)
if [ "$cutoff" -gt 0 ]; then
  for f in 00-inbox/*.md; do
    mt=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
    [ "$mt" -gt 0 ] && [ "$mt" -lt "$cutoff" ] && stale=$((stale + 1))
  done
fi
[ "$stale" -gt 0 ] && flags+=("в 00-inbox/ $stale запис(ь/и) старше недели → триаж strict (80-kernel/docs/inbox-triage.md)")

# 3. Незакоммиченное дерево — не нарушение ритма, но частая причина потери канвы.
if ! git diff --quiet HEAD -- 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  flags+=("незакоммиченные изменения в vault → /checkpoint")
fi

if [ ${#flags[@]} -gt 0 ]; then
  echo "⚠ Детектор ритма (INV-5/INV-9) — открытые рубежи:"
  for fl in "${flags[@]}"; do echo "  • $fl"; done
fi
exit 0
