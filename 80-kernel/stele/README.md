# Стела — реестр архитектурных решений (ADR)

> Στήλη — каменная плита, на которой высекали декреты для постоянного публичного учёта.
> Здесь система документирует саму себя: каждое решение о её устройстве датировано, обосновано и связано с инвариантами контракта. Решения не переписываются молча — отменяются только новым ADR (статус `superseded ADR-NNNN`).

## Зачем

- **INV-17 (система-как-код):** vault держит собственную архитектуру внутри себя, а не в голове инженера.
- **Один канон:** карточка задачи, скилл или заметка **ссылаются** на решение, а не пересказывают его (INV-2).
- **Контракт:** инварианты `INV-N` — в [`contract.md`](contract.md); ADR ссылаются туда, а не переопределяют.

## Формат

Один файл на решение: `ADR-NNNN-slug.md` по [`../scaffolds/adr-tmpl.md`](../scaffolds/adr-tmpl.md). Статусы: `proposed` / `accepted` / `superseded ADR-MMMM` / `withdrawn`. Имена — по ADR-0003.

Значимое архитектурное решение проходит `/archgate` **до** записи ADR: профиль по семи характеристикам с вето-фильтром, а ADR фиксирует результат. Тривиальное и обратимое решение ADR не требует.

## Дом ADR

- Решение **об этой системе** (раскладка, гейты, конвенции, машинерия) → сюда, `80-kernel/stele/`.
- Решение **о рабочей системе, которую ты развиваешь** (сервис, кластер, пайплайн) → `10-governance/projects/<проект>/adr/NNNN-slug.md`, а не в репозиторий самой системы: ADR раскрывает топологию, провайдера и расположение секретов, и в общедоступном репозитории это лишнее. Если у команды есть свой канон ADR — их правила старше этого.

## Реестр

| # | Решение | Статус | Инварианты |
|---|---------|--------|-----------|
| [0001](ADR-0001-vault-as-substrate.md) | Vault как единственный субстрат | accepted | INV-1 INV-3 INV-4 INV-7 |
| [0002](ADR-0002-topology-flat-core.md) | Топология: плоское ядро + dot-зона | accepted | INV-1 INV-3 INV-7 |
| [0003](ADR-0003-naming-convention.md) | Конвенция именования | accepted | INV-17 INV-18 |
| [0004](ADR-0004-agent-machinery-in-dotclaude.md) | Машинерия агента в `.claude/` | accepted | INV-17 INV-18 |
| [0005](ADR-0005-memory-native-in-repo.md) | Память в репо через нативный механизм | accepted | INV-1 INV-7 INV-17 |
| [0006](ADR-0006-tracker-ticket-as-unit.md) | Тикет трекера как единица учёта работы | accepted | INV-2 INV-3 INV-14 INV-22 |
| [0007](ADR-0007-metadata-convention.md) | Конвенция метаданных | accepted | INV-11 INV-17 INV-18 |
| [0008](ADR-0008-template-kinds.md) | Два рода шаблонов: Templater ≠ agent-скелет | accepted | INV-4 INV-18 INV-19 |
| [0009](ADR-0009-pre-commit-gates.md) | Git-гейты через pre-commit | accepted | INV-5 INV-17 INV-22 |
| [0010](ADR-0010-installation-config.md) | Конфиг установки (`80-kernel/config.md`) | accepted | INV-1 INV-3 INV-18 |
| [0011](ADR-0011-fpf-submodule-no-mcp.md) | FPF как submodule, без внешнего MCP | accepted | INV-1 INV-6 INV-7 INV-16 |
| [0012](ADR-0012-obsidian-plugins-not-vendored.md) | Плагины Obsidian не вендорятся в git | accepted | INV-1 INV-3 INV-18 |
| [0013](ADR-0013-workspace-layout-via-snapshot.md) | Раскладка Obsidian: именованный снимок, не живой `workspace.json` | accepted | INV-1 INV-3 |

> Даты в шапках ADR — плейсхолдеры `<YYYY-MM-DD>`. При развёртывании проставь дату принятия: решение без даты не решение, а мнение.
