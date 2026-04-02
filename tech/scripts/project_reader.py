import os
import sys
import fnmatch
from pathlib import Path
from datetime import datetime


def should_exclude(path: Path, exclude_patterns: list[str]) -> bool:
    """Проверяет, нужно ли исключить файл/директорию"""
    # Проверяем по имени
    if any(part in exclude_patterns for part in path.parts):
        return True

    # Проверяем по маске
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            return True

    return False


def collect_all_files(directory: Path, exclude_patterns: list[str]) -> list[Path]:
    """Собирает все файлы, кроме исключённых"""
    all_files = []

    for file_path in directory.rglob("*"):
        # Пропускаем если файл в исключённой папке
        if should_exclude(file_path, exclude_patterns):
            continue

        # Пропускаем если не файл
        if not file_path.is_file():
            continue

        all_files.append(file_path)

    return sorted(all_files)


def get_file_category(file_path: Path) -> str:
    """Определяет категорию файла по расширению"""
    ext = file_path.suffix.lower()

    if ext in ['.py']:
        return 'python'
    elif ext in ['.ini', '.cfg', '.conf']:
        return 'config'
    elif ext in ['.yaml', '.yml']:
        return 'yaml'
    elif ext in ['.json']:
        return 'json'
    elif ext in ['.md', '.rst', '.txt']:
        return 'docs'
    elif ext in ['.sql']:
        return 'sql'
    elif ext in ['.sh', '.bat', '.ps1']:
        return 'scripts'
    elif ext in ['.toml']:
        return 'toml'
    elif ext in ['.lock']:
        return 'lock'
    elif ext in ['.gitignore', '.dockerignore', '.pre-commit-config.yaml']:
        return 'git'
    elif file_path.name in ['Dockerfile', 'Makefile']:
        return 'build'
    else:
        return 'other'


def collect_project_files(directory: str, output_file: str):
    """Собирает все файлы проекта в один файл"""

    base_path = Path(directory).resolve()

    if not base_path.exists():
        print(f"Ошибка: Директория '{directory}' не существует!")
        return False

    # Паттерны для исключения
    exclude_patterns = [
        '.git', '__pycache__', '.pytest_cache', '.mypy_cache',
        'venv', 'env', '.venv', '.env',
        'tech/venv',  # 👈 добавить! виртуалка
        '*.pyc', '*.pyo', '*.so', '*.dll', '*.exe',
        '*.db', '*.sqlite', '*.sqlite3',
        '*.log', '*.pid',
        '.DS_Store', 'Thumbs.db',
        'project_full_dump.txt',  # сам себя не включаем
        'all_python_files.txt',
        'node_modules', '.idea', '.vscode',
    ]

    # Собираем все файлы
    all_files = collect_all_files(base_path, exclude_patterns)

    if not all_files:
        print(f"Файлы не найдены в '{directory}'")
        return False

    # Группируем по категориям
    files_by_category = {}
    for file_path in all_files:
        category = get_file_category(file_path)
        files_by_category.setdefault(category, []).append(file_path)

    try:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            # Заголовок
            out_file.write(f"{'=' * 80}\n")
            out_file.write(f"СБОРКА ВСЕХ ФАЙЛОВ ПРОЕКТА\n")
            out_file.write(f"Директория: {base_path}\n")
            out_file.write(f"Всего файлов: {len(all_files)}\n")
            out_file.write(f"Дата создания: {datetime.now()}\n")
            out_file.write(f"{'=' * 80}\n\n")

            # Статистика по категориям
            out_file.write("СТАТИСТИКА ПО КАТЕГОРИЯМ:\n")
            out_file.write("-" * 40 + "\n")
            for category, files in sorted(files_by_category.items()):
                out_file.write(f"  {category.upper()}: {len(files)} файлов\n")
            out_file.write(f"\n{'=' * 80}\n\n")

            # Обрабатываем каждую категорию
            for category, files in sorted(files_by_category.items()):
                out_file.write(f"\n{'█' * 80}\n")
                out_file.write(f"КАТЕГОРИЯ: {category.upper()}\n")
                out_file.write(f"{'█' * 80}\n\n")

                for i, file_path in enumerate(files, 1):
                    try:
                        rel_path = file_path.relative_to(base_path)

                        out_file.write(f"{'─' * 80}\n")
                        out_file.write(f"Файл {i}/{len(files)}: {rel_path}\n")
                        out_file.write(f"Полный путь: {file_path}\n")
                        out_file.write(f"Категория: {category}\n")
                        out_file.write(f"{'─' * 80}\n")

                        # Читаем содержимое
                        try:
                            with open(file_path, 'r', encoding='utf-8') as in_file:
                                content = in_file.read()
                            out_file.write(content)
                        except UnicodeDecodeError:
                            # Бинарные файлы
                            out_file.write(f"\n[БИНАРНЫЙ ФАЙЛ — содержимое не отображается]\n")
                        except Exception as e:
                            out_file.write(f"\n[ОШИБКА ЧТЕНИЯ: {e}]\n")

                        # Разделитель
                        if i < len(files):
                            out_file.write(f"\n\n{'=' * 80}\n")
                            out_file.write(f"Конец файла: {rel_path}\n")
                            out_file.write(f"{'=' * 80}\n\n")
                        else:
                            out_file.write(f"\n\n{'=' * 80}\n")
                            out_file.write(f"Конец последнего файла в категории: {rel_path}\n")
                            out_file.write(f"{'=' * 80}\n")

                        print(f"✓ {category}: {rel_path}")

                    except Exception as e:
                        error_msg = f"Ошибка при обработке {file_path}: {e}"
                        print(f"✗ {error_msg}")
                        out_file.write(f"\n[ОШИБКА] {error_msg}\n\n")

            print(f"\n✅ Готово! Все файлы собраны в: {output_file}")
            print(f"Всего обработано: {len(all_files)} файлов")
            return True

    except Exception as e:
        print(f"Ошибка при записи в выходной файл: {e}")
        return False


def main():
    script_path = Path(__file__).resolve()

    if script_path.parent.name == 'scripts' and script_path.parent.parent.name == 'tech':
        start_dir = script_path.parent.parent.parent
    else:
        start_dir = Path.cwd()

    # Имя выходного файла
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = str(start_dir / "project_full_dump.txt")

    print(f"Сканирование: {start_dir}")
    print(f"Результат: {output_file}")
    print("-" * 50)

    collect_project_files(str(start_dir), output_file)


if __name__ == "__main__":
    main()