import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.infrastructure.Base import Base


class Database:
    def __init__(self):
        root = os.environ.get("PROJECT_ROOT")
        if root:
            BASE_DIR = Path(root)
        else:
            BASE_DIR = Path(__file__).parent.parent.parent.parent

        DB_PATH = BASE_DIR / "data" / "app.db"

        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        engine = create_engine(f"sqlite:///{DB_PATH}")
        Base.metadata.create_all(bind=engine)

        self.session = sessionmaker(bind=engine)
