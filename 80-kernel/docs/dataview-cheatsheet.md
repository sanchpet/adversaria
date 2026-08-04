---
type: system
aliases: ["Dataview шпаргалка", "Проекции"]
---

# Dataview — шпаргалка проекций

> Проекции читают frontmatter карточек и ничего не хранят (INV-11: место-вид, не источник). Схема полей — [[ADR-0007-metadata-convention|ADR-0007]].
> Запрос не работает — сначала проверь frontmatter карточки, а не запрос: в девяти случаях из десяти дело в опечатке в `type` или `status`.

## Активные задачи

````
```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title AS "Задача", status AS "Статус", link(project) AS "Проект"
FROM "10-governance/tasks"
WHERE type = "task" AND status != "done"
SORT status ASC, file.name ASC
```
````

## Задачи одного проекта

````
```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title, status, artifact AS "Артефакт"
FROM "10-governance/tasks"
WHERE type = "task" AND contains(string(project), "имя-проекта")
SORT status ASC
```
````

## Заблокированные — что ждёт не меня

````
```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title, depends_on AS "Ждёт"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "blocked"
```
````

## Детектор разрыва трассировки (INV-14)

````
```dataview
LIST "задача без проекта"
FROM "10-governance/tasks"
WHERE type = "task" AND !project AND status != "done"
```
````

## Проекты

````
```dataview
TABLE WITHOUT ID link(file.link, file.aliases[0]) AS "Проект", status AS "Статус", goal AS "Цель работодателя"
FROM "10-governance/projects"
WHERE type = "project"
SORT status ASC
```
````

## Что закрыто за неделю

````
```dataview
TABLE WITHOUT ID link(file.link, ticket) AS "Тикет", title, closed AS "Закрыто"
FROM "10-governance/tasks"
WHERE type = "task" AND status = "done" AND closed >= date(today) - dur(7 days)
SORT closed DESC
```
````

## Инбокс старше недели (кандидаты в архив)

````
```dataview
LIST file.ctime
FROM "00-inbox"
WHERE file.ctime <= date(today) - dur(7 days)
SORT file.ctime ASC
```
````

## Приёмы

- `WITHOUT ID` убирает колонку ссылки по умолчанию — нужен всегда, когда первую колонку строишь сам.
- `link(file.link, ticket)` показывает тикет вместо имени файла: имя строчное (ADR-0003), а читать хочется каноническое.
- `contains(string(x), "…")` устойчив к тому, что поле может быть и ссылкой, и строкой.
- Даты сравниваются как `date(today) - dur(7 days)`; строковое сравнение дат работает, пока формат `YYYY-MM-DD`, и ломается молча, если формат уехал.
- **Bases** (нативные доски) удобнее dataview там, где нужна группировка карточками — см. `10-governance/tasks.base`. Dataview остаётся для таблиц и детекторов.
