---
type: registry-index
aliases: [Реестр, Карта, Стартовая]
---

# Реестр — карта работы

> Это **вид** поверх frontmatter карточек, не дубль (INV-11: место-вид, не источник). Трассировка: цель работодателя → проект → задача → тикет.
> Запрос ничего не показывает — проверь сначала frontmatter карточки, а не запрос.

## Задачи в работе

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

> Блокер, который никто не толкает, — это не блокер, а отложенная задача. Разбор — на своде недели.

## Доска задач

> Нативная доска Bases — карточки, сгруппированные по статусу. Виды переключаются сверху.

![[tasks.base]]

## Проекты

```dataview
TABLE WITHOUT ID link(file.link, file.aliases[0]) AS "Проект", status AS "Статус", goal AS "Цель"
FROM "10-governance/projects"
WHERE type = "project"
SORT status ASC
```

## Детектор разрыва трассировки

```dataview
LIST "задача без проекта"
FROM "10-governance/tasks"
WHERE type = "task" AND !project AND status != "done"
```

> Разрыв не ошибка данных. Это вопрос: действительно ли ты занят тем, чем считаешь себя занятым.

## Закрыто за последнюю неделю

```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title AS "Задача", closed AS "Закрыто"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "done" AND closed >= date(today) - dur(7 days)
SORT closed DESC
```
