import os


def is_hidden(name: str) -> bool:
    """Папки/файлы, начинающиеся с точки, считаем скрытыми."""
    return name.startswith('.') and name not in ('.', '..')


def write_tree(root_path: str, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Просто заголовок текстом, без markdown-символов
        f.write(f"Project structure: {os.path.basename(root_path)}\n\n")
        _walk(root_path, f, prefix="")


def _walk(path: str, file_handle, prefix: str):
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return

    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = (i == len(entries) - 1)

        connector = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "

        # Скрытые папки — не раскрываем, только отмечаем
        if is_hidden(entry) and os.path.isdir(full_path):
            file_handle.write(prefix + connector + entry + "  *hidden*\n")
            continue

        if os.path.isfile(full_path):
            file_handle.write(prefix + connector + entry + "\n")
            continue

        # Папка
        file_handle.write(prefix + connector + entry + "/\n")
        _walk(full_path, file_handle, prefix + next_prefix)


if __name__ == "__main__":
    # Скрипт лежит в /scripts, поднимаемся в корень проекта
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_path = os.path.join(project_root, "project_documentation", "project_structure.md")

    write_tree(project_root, output_path)
    print("Project structure updated:", output_path)
