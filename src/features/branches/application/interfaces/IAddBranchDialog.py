from abc import ABC, abstractmethod
from typing import Callable


class IAddBranchDialog(ABC):
    @abstractmethod
    def set_on_branch_data_entered(self, callback: Callable[[dict], None]):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
