#!/usr/bin/env python3
"""Проверка внешних ссылок перед публикацией. Норма — `/corp-docs`, шаг 1.

Битая ссылка в вики хуже отсутствующей: она обещает ответ, которого нет. Норма
требовала верифицировать ссылки, но проверялась глазами, то есть не проверялась.

Вход: файлы или текст на stdin. Выход: строка на каждую ссылку, которая не
ответила. Exit 0 — все живы или ни одной не нашлось; exit 1 — есть мёртвые.

Рубежом на публикации это не стоит (сеть в хуке платится задержкой на каждую
отправку и ломается без сети), поэтому — отдельный прогон.

  python3 80-kernel/scripts/link-check.py draft.md
  pbpaste | python3 80-kernel/scripts/link-check.py

HEAD с фолбэком на GET: часть площадок отвечает 405 на HEAD, и это не поломка
ссылки. 401 и 403 тоже не поломка — за ними живая страница под аутентификацией,
и о них сообщается отдельной пометкой, а не отказом.

Граница проверки: она отвечает «адрес отзывается», а не «там та страница».
Аутентификационный шлюз, отдающий 200 на своей форме входа, отсюда неотличим
от целевой страницы и проходит молча — наблюдалось. Для ссылок за таким шлюзом
проверка не доказывает ничего.
"""
import concurrent.futures
import re
import sys
import urllib.error
import urllib.request

URL_RE = re.compile(r"https?://[^\s<>\"'`)\]}]+")
TIMEOUT = 10
AGENT = "link-check/1.0"
AUTH_CODES = {401, 403}


def probe(url):
    """(url, код или None, пояснение). None в коде — соединение не состоялось."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return url, resp.status, ""
        except urllib.error.HTTPError as e:
            if e.code == 405 and method == "HEAD":
                continue
            return url, e.code, e.reason or ""
        except urllib.error.URLError as e:
            return url, None, str(e.reason)
        except (TimeoutError, OSError) as e:
            return url, None, str(e)
    return url, None, "HEAD и GET оба без ответа"


def main():
    if sys.argv[1:]:
        text = ""
        for path in sys.argv[1:]:
            try:
                with open(path, encoding="utf-8") as fh:
                    text += fh.read() + "\n"
            except OSError as e:
                print(f"не читается: {path}: {e}", file=sys.stderr)
                return 1
    else:
        text = sys.stdin.read()

    urls = sorted({u.rstrip(".,;:") for u in URL_RE.findall(text)})
    if not urls:
        print("внешних ссылок не найдено")
        return 0

    dead, gated = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, code, note in pool.map(probe, urls):
            if code is None:
                dead.append(f"  нет ответа  {url}  ({note})")
            elif code in AUTH_CODES:
                gated.append(f"  {code}         {url}  (живая, за аутентификацией)")
            elif code >= 400:
                dead.append(f"  {code}         {url}  {note}")

    print(f"проверено ссылок: {len(urls)}")
    if gated:
        print("за аутентификацией — проверить руками, что это та страница:")
        print("\n".join(gated))
    if dead:
        print("не отвечают:")
        print("\n".join(dead))
        return 1
    print("все живы")
    return 0


if __name__ == "__main__":
    sys.exit(main())
