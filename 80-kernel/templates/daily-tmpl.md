<%*
// Templater — потребитель ЧЕЛОВЕК (ADR-0008). Агент этот файл не использует.
const m = moment();
const fileName = m.format("YYYY-MM-DD");
await tp.file.move(`20-library/notes/${fileName}`);
-%>
---
type: note
status: later
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% tp.date.now("dddd, D MMMM YYYY") %>

<% tp.file.cursor(1) %>
