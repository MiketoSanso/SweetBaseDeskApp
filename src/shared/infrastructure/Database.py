import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Database:
    def __init__(self):
        root = os.environ.get("PROJECT_ROOT")
        if root:
            BASE_DIR = Path(root)
        else:
            BASE_DIR = Path(__file__).parent.parent.parent.parent

        DB_PATH = BASE_DIR / "data" / "app.db"

        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._engine = create_engine(f"sqlite:///{DB_PATH}")
        self._session_local = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self._session_local()

    @property
    def engine(self):
        return self._engine
