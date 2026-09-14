---
type: registry-index
aliases: [Старт, Стартовая, Рабочий стол]
cssclasses:
  - hide-properties
---

# Рабочий стол

> Стартовая страница (INV-11): **место-вид, не источник**. Всё ниже читается из frontmatter карточек и ничего не хранит. Пусто в секции — значит пусто в системе, а не «запрос сломался»; но если сомневаешься, проверяй сначала frontmatter карточки, а не запрос.

## Сегодня

```dataview
LIST
FROM "10-governance/plans/current"
WHERE type = "dayplan"
SORT file.name DESC
LIMIT 1
```

> Плана на день нет → `/open`. Вчерашний план остался здесь → вчера не закрыт, `/close`.

## В работе

```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title AS "Задача", link(project) AS "Проект", verification_class AS "Класс"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "in-progress"
SORT priority DESC, file.name ASC
```

## Ждут не меня

```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title AS "Задача", depends_on AS "Ждём"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "blocked"
SORT file.name ASC
```

> Блокер, который никто не толкает, — не блокер, а отложенная задача. Разбор — на своде недели.

## Доска

![[tasks.base]]

## Проекты по приоритету

> `priority` 1–5, **1 высший**; степень, а не ранг — два проекта могут делить уровень. Назначает инженер, агент не переставляет. Порядок отсюда — вход в вёрстку недели: `/open` строит WeekPlan от него, а не от объёма остатков.

```dataview
TABLE WITHOUT ID link(file.link, file.aliases[0]) AS "Проект", priority AS "🚦", status AS "Статус", goal AS "Цель"
FROM "10-governance/projects"
WHERE type = "project" AND status != "done"
SORT priority ASC, status ASC
```

## Детекторы

> Не ошибки, а вопросы к себе. Молчат — всё в порядке.

**Задачи без проекта** — действительно ли ты занят тем, чем считаешь себя занятым:

```dataview
LIST
FROM "10-governance/tasks"
WHERE type = "task" AND !project AND status != "done"
```

**Проект без приоритета** — порядок недели не из чего собрать, и вёрстка молча вернётся к объёму остатков:

```dataview
LIST
FROM "10-governance/projects"
WHERE type = "project" AND status != "done" AND !priority
```

**Инбокс старше недели** — род не присвоен за полный проход, ценность не подтверждена (→ `90-archive/`):

```dataview
LIST file.mtime
FROM "00-inbox"
WHERE file.mtime <= date(today) - dur(7 days)
SORT file.mtime ASC
```

**Отложенное** — то, что решили не делать сейчас; проверить, не стало ли оно нужным:

```dataview
LIST
FROM "10-governance/tasks"
WHERE type = "task" AND status = "later"
```

## Закрыто за неделю

```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title AS "Задача", closed AS "Закрыто"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "done" AND closed >= date(today) - dur(7 days)
SORT closed DESC
```

---

**День:** `/open` → работа → `/checkpoint` → `/close`  ·  **Работа:** `/task` · `/verify`  ·  **Решение:** `/think` · `/archgate` · `/fpf`  ·  **Текст коллегам:** `/corp-docs`

Дисциплина задач — [[task-discipline]] · Триаж инбокса — [[inbox-triage]] · Архитектура — [Стела](80-kernel/stele/README.md) · Инварианты — [[contract]]
