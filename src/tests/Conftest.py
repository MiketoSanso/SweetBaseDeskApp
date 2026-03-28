import os
import sys
import tempfile
from pathlib import Path

import pytest
from PySide6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Dependencies import Dependencies
from src.shared.infrastructure.Base import Base
from src.shared.infrastructure.Database import Database


@pytest.fixture(scope="session")
def qapp():
    app = QApplication(sys.argv)
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db_path = f.name

    engine = create_engine(f"sqlite:///{temp_db_path}")
    Base.metadata.create_all(engine)

    original_session = Database.session()
    Database.session = sessionmaker(bind=engine)

    yield engine

    Database.session = original_session
    os.unlink(temp_db_path)


@pytest.fixture
def dependencies(temp_db):
    original_env = os.environ.get("PROJECT_ROOT")
    os.environ["PROJECT_ROOT"] = str(Path(__file__).parent.parent)

    deps = Dependencies()

    deps.db = Database
    deps.db.session = sessionmaker(bind=temp_db)

    deps.initlialize_data()
    deps.initialize_usecases()

    if original_env:
        os.environ["PROJECT_ROOT"] = original_env


@pytest.fixture
def main_window(qapp, dependencies):
    window = dependencies.main_window
    window.show()
    yield window
    window.close()
