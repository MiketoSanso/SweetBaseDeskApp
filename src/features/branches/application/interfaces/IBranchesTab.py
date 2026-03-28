from abc import ABC, abstractmethod
from typing import Callable


class IBranchesTab(ABC):
    @abstractmethod
    def set_on_add_branch_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_load_branches_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def display_branches(self, branches, is_available):
        pass
