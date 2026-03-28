import sys

from src.shared.infrastructure.LoggerController import LoggerController

import os

from Dependencies import Dependencies
from pathlib import Path

from src.shared.presentation.Window import Window

os.environ['PROJECT_ROOT'] = str(Path(__file__).parent)

def main():
    logger = LoggerController()
    logger.setup_logging()

    window = Window()
    dependencies = Dependencies()

    main_window = dependencies.main_window
    main_window.show()

    window.exit()


if __name__ == "__main__":
    main()