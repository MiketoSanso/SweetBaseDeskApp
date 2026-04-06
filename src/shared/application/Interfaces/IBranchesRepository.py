from abc import ABC, abstractmethod

from src.features.branches.domain.entities.Branch import Branch
from src.shared.infrastructure.Database import Database


class IBranchesRepository(ABC):
    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def get_branches(self) -> list[Branch]:
        pass

    @abstractmethod
    def delete_branch(self, id: str) -> bool:
        pass

    @abstractmethod
    def add_branch(self, branch: Branch):
        pass

    @abstractmethod
    def get_branch_by_id(self, id: int) -> Branch:
        pass

    @abstractmethod
    def change_branch_by_id(self, id: int, new_branch: Branch) -> bool:
        pass
