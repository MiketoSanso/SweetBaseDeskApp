import os
import sys
from pathlib import Path


def collect_python_files(directory, output_file):
    """
    Собирает все Python-файлы из директории и всех поддиректорий,
    и объединяет их в один файл с указанием источника.
    """

    # Используем Path для кроссплатформенной работы
    base_path = Path(directory).resolve()

    # Проверяем существование директории
    if not base_path.exists():
        print(f"Ошибка: Директория '{directory}' не существует!")
        return False

    # Собираем все .py файлы
    python_files = []

    # Используем rglob для рекурсивного поиска
    for py_file in base_path.rglob("*.py"):
        # Исключаем виртуальные окружения и скрытые папки
        if any(part.startswith('.') or part in ['venv', 'env', '.venv', '.env', '__pycache__']
               for part in py_file.parts):
            continue
        python_files.append(py_file)

    if not python_files:
        print(f"Python-файлы не найдены в '{directory}' и его подпапках")
        return False

    try:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            # Записываем заголовок
            out_file.write(f"{'=' * 80}\n")
            out_file.write(f"Сборка Python-файлов из: {base_path}\n")
            out_file.write(f"Всего найдено файлов: {len(python_files)}\n")
            out_file.write(f"Дата создания: {__import__('datetime').datetime.now()}\n")
            out_file.write(f"{'=' * 80}\n\n")

            # Обрабатываем каждый файл
            for i, file_path in enumerate(sorted(python_files), 1):
                try:
                    # Получаем относительный путь
                    rel_path = file_path.relative_to(base_path)

                    # Записываем информацию о файле
                    out_file.write(f"{'─' * 80}\n")
                    out_file.write(f"Файл {i}/{len(python_files)}: {rel_path}\n")
                    out_file.write(f"Полный путь: {file_path}\n")
                    out_file.write(f"{'─' * 80}\n")

                    # Читаем содержимое файла
                    with open(file_path, 'r', encoding='utf-8') as in_file:
                        content = in_file.read()

                    # Записываем содержимое
                    out_file.write(content)

                    # Добавляем разделитель между файлами
                    if i < len(python_files):
                        out_file.write(f"\n\n{'=' * 80}\n")
                        out_file.write(f"Конец файла: {rel_path}\n")
                        out_file.write(f"{'=' * 80}\n\n")
                    else:
                        out_file.write(f"\n\n{'=' * 80}\n")
                        out_file.write(f"Конец последнего файла: {rel_path}\n")
                        out_file.write(f"{'=' * 80}\n")

                    print(f"✓ Обработан: {rel_path}")

                except Exception as e:
                    error_msg = f"Ошибка при чтении {file_path}: {str(e)}"
                    print(f"✗ {error_msg}")
                    out_file.write(f"\n[ОШИБКА] {error_msg}\n\n")

            print(f"\n✅ Готово! Файлы собраны в: {output_file}")
            return True

    except Exception as e:
        print(f"Ошибка при записи в выходной файл: {str(e)}")
        return False


def main():
    # Если передан аргумент командной строки, используем его как директорию
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        # Иначе используем текущую директорию
        start_dir = os.getcwd()

    # Имя выходного файла
    output_file = "all_python_files.txt"

    # Если передан второй аргумент, используем его как имя выходного файла
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    print(f"Поиск Python-файлов в: {start_dir}")
    print(f"Результат будет сохранен в: {output_file}")
    print("-" * 50)

    collect_python_files(start_dir, output_file)


if __name__ == "__main__":
    main()