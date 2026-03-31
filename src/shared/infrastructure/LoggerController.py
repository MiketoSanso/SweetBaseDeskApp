import logging
import sys
from pathlib import Path


class LoggerController:
    def setup_logging(self):
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_dir / "app.log", encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

