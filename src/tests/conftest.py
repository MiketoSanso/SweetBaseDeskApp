import os
import sys
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.shared.infrastructure.Base import Base
from src.shared.infrastructure.Database import Database


@pytest.fixture(scope="session")
def qapp():
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db_path = f.name

    engine = create_engine(f"sqlite:///{temp_db_path}")
    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()

    import time

    time.sleep(0.1)
    os.unlink(temp_db_path)


@pytest.fixture
def dependencies(temp_db, qapp):  # 👈 qapp нужен для Qt
    from Dependencies import Dependencies

    original_env = os.environ.get("PROJECT_ROOT")
    os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

    deps = Dependencies()

    # Подменяем БД
    deps.db = Database()
    deps.db._engine = temp_db
    deps.db._session_local = sessionmaker(bind=temp_db)

    deps.initialize_data()
    deps.initialize_usecases()

    yield deps

    if original_env:
        os.environ["PROJECT_ROOT"] = original_env
    else:
        del os.environ["PROJECT_ROOT"]


@pytest.fixture
def main_window(qapp, dependencies):
    window = dependencies.main_window
    window.show()
    yield window
    window.close()
