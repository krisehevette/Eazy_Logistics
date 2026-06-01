import os
import re

FILES_TO_INCLUDE = {
    "architecture_overview.md": True,
    "project_structure.md": True,
    "project_log.md": False,
    "todo_list.md": False,
    "UI_architecture.md": True,
    "UI_context.md": True,
    "rendering_pipeline.md": True,
    "core_context.md": True,
    "event_bus.md": True,
    "application_initialization.md": True,
    "application_main_loop.md": False,
    "application_shutdown.md": False,
    "application_startup.md": True
}

DOCS_DIR = "project_documentation"
# MAIN_FILE = "project_context.md"  
# MAIN_FILE = "UI/UI_context.md"
MAIN_FILE = "Core/application_initialization.md"
OUTPUT_FILE = os.path.join(DOCS_DIR, "all_doc.md")

HEADER_RE = re.compile(r"^(#+)\s")


def extract_md_links(line: str):
    """
    Ищет ссылки вида:
    [текст](/project_documentation/.../filename.md)
    Возвращает путь относительно DOCS_DIR: "filename.md" или "UI/UI_context.md".
    """
    match = re.search(r"\[[^\]]+\]\(/project_documentation/(.+?\.md)\)", line)
    if not match:
        return None
    return match.group(1).replace("\\", "/")


def quote_line(line: str, depth: int) -> str:
    """
    depth=1 → "> текст"
    depth=2 → ">> текст"
    depth=3 → ">>> текст"
    Пустая строка → просто ">" или ">>" без пробела.
    """
    if line == "":
        return ">" * depth
    return f"{'>' * depth} {line}"


def expand_file(filename: str, depth: int) -> str:
    """
    Рекурсивно раскрывает файл с учётом глубины цитирования.
    depth — уровень вложенности цитат:
      1 → >
      2 → >>
      3 → >>>
    """
    full_path = os.path.join(DOCS_DIR, filename)

    if not os.path.exists(full_path):
        return quote_line(f"⚠ Файл не найден: {filename}", depth)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    result_lines = []
    lines = content.splitlines()

    current_header_level = 1

    for line in lines:
        # обновляем текущий уровень заголовка
        m = HEADER_RE.match(line)
        if m:
            current_header_level = len(m.group(1))

        link = extract_md_links(line)

        if link:
            short_name = os.path.basename(link)

            # строку с ссылкой сохраняем, но в цитате
            result_lines.append(quote_line(line, depth))

            # если файл не включаем — на этом всё
            if not FILES_TO_INCLUDE.get(short_name, False):
                continue

            # пустая строка внутри цитаты перед заголовком
            result_lines.append(quote_line("", depth))

            # заголовок "Содержимое файла ..." — ВНЕ цитаты
            header_level = current_header_level + 1
            header_line = "#" * header_level + f" Содержимое файла {short_name}:"
            result_lines.append(header_line)

            # сразу после заголовка — содержимое вложенного файла в более глубокой цитате
            nested = expand_file(link, depth + 1)
            result_lines.append(nested)

        else:
            # обычная строка → цитируем на текущей глубине
            result_lines.append(quote_line(line, depth))

    return "\n".join(result_lines)


def build_document():
    main_path = os.path.join(DOCS_DIR, MAIN_FILE)

    with open(main_path, "r", encoding="utf-8") as f:
        main_text = f.read()

    output = []
    lines = main_text.splitlines()

    current_header_level = 1

    for line in lines:
        # обновляем текущий уровень заголовка
        m = HEADER_RE.match(line)
        if m:
            current_header_level = len(m.group(1))

        link = extract_md_links(line)

        if not link:
            # строка без ссылки — просто переписываем
            output.append(line)
            continue

        short_name = os.path.basename(link)

        # строку с ссылкой сохраняем как есть
        output.append(line)

        # если файл не включаем — просто идём дальше
        if not FILES_TO_INCLUDE.get(short_name, False):
            continue

        # заголовок "Содержимое файла ..." в основном файле
        header_level = current_header_level + 1
        header_line = "#" * header_level + f" Содержимое файла {short_name}:"
        output.append(header_line)

        # сразу после заголовка — цитируемое содержимое вложенного файла
        nested = expand_file(link, 1)
        output.append(nested)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    build_document()
    print("Готово! Документация собрана.")
