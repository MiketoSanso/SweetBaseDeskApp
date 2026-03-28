from abc import ABC, abstractmethod
from typing import Callable


class IReportsTab(ABC):
    @abstractmethod
    def set_on_open_reports_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def display_stats(self, stats):
        pass
