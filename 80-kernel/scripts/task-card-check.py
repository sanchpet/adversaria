#!/usr/bin/env python3
"""Гейт карточки задачи (ADR-0006): карточка не регистрируется без тикета и без
предъявимого артефакта.

Вход: имена файлов аргументами (pre-commit передаёт staged-файлы) ИЛИ markdown из
stdin (fallback для хука гарнитуры, у которого файла на диске ещё нет).
Exit 0 — валидно; exit 2 — нет (с сообщением в stderr).

Невалидно: нет frontmatter; нет поля ticket/artifact; пустое значение; незаполненный
плейсхолдер шаблона (<...>); формулировка-деятельность вместо артефакта.
"""
import re
import sys

# Деятельность ≠ артефакт. Ловим самые частые формулировки — не как полный словарь,
# а как напоминание о тесте «что предъявлю».
ACTIVITY = (
    "разобрал", "разобрат", "посмотр", "поработа", "изуч", "почита",
    "вник", "ознаком", "поуча", "поню", "покопа",
)


def _field(fm, name):
    m = re.search(rf"^{name}:\s*(.*)$", fm, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'").strip()


def check(txt, label):
    m = re.match(r"---\n(.*?)\n---", txt, re.S)
    if not m:
        return f"{label}: ADR-0006 — карточка задачи без frontmatter (нет ticket/artifact)."
    fm = m.group(1)

    ticket = _field(fm, "ticket")
    if not ticket or ("<" in ticket and ">" in ticket):
        return (f"{label}: ADR-0006 — карточка не заводится без тикета. Заполни `ticket:`. "
                "Работа без тикета живёт в трекере или в 00-inbox/, но не карточкой: "
                "собственная нумерация дала бы второй идентификатор одной работы.")

    artifact = _field(fm, "artifact")
    if not artifact or ("<" in artifact and ">" in artifact):
        return (f"{label}: ADR-0006 — карточка не заводится без предъявимого артефакта. "
                "Заполни `artifact:` — что покажешь как доказательство, что работа сделана "
                "(репозиторий, коммит, конфиг, развёрнутый сервис, документ, дашборд, разбор с выводом). "
                "Тест: «что я предъявлю?»")

    low = artifact.lower()
    if any(low.startswith(a) or f" {a}" in low for a in ACTIVITY):
        return (f"{label}: ADR-0006 — `artifact` описывает деятельность, а не результат ({artifact!r}). "
                "«Разобрался / посмотрел / поработал» предъявить нельзя. Назови выход: "
                "что останется в мире, когда работа кончится.")
    return None


def main():
    errs = []
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            try:
                with open(p, encoding="utf-8") as f:
                    txt = f.read()
            except OSError as e:
                errs.append(f"{p}: не прочитан ({e})")
                continue
            e = check(txt, p)
            if e:
                errs.append(e)
    else:
        e = check(sys.stdin.read(), "<stdin>")
        if e:
            errs.append(e)

    if errs:
        for e in errs:
            sys.stderr.write(e + "\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
