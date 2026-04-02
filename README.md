# SweetBaseDeskApp
Desktop app for marketplace business


---


## Инструкция по установке:
ПЕРВЫЙ ЗАПУСК: tech\scripts\setup.bat

---

## Инструкция по дополнению:
1) Указывать новые библиотеки в tech\.config\requirements.txt
2) Указывать обязательные действия перед коммитом в tech\.config\.pre-commit-config.yaml

---

### Тех. подробности работы:

1) tech/.config:
1.1) .pre-commit-config.yaml - настраивает действия перед коммитом.
1.2) alembic.ini - настраивает параметры миграций
1.3) requirements.txt - хранит все библиотеки для автозагрузки
2) tech/scripts:
2.1) project_reader.py - собирает все файлы в текст для обработки в AI
2.2) setup.bat - создаёт venv, устанавливает зависимости из конфига 1.3, запускает первую миграцию через конфиг 1.2, прокидывает конфиг 1.1) в расширение.

---