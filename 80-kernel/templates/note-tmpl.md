<%*
// Templater — потребитель ЧЕЛОВЕК (ADR-0008).
const title = await tp.system.prompt("Заголовок заметки");
const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
await tp.file.rename(slug || tp.date.now("YYYY-MM-DD-HHmm"));
-%>
---
type: note
status: later
created: <% tp.date.now("YYYY-MM-DD") %>
aliases: ["<% title %>"]
---

# <% title %>

<% tp.file.cursor(1) %>
