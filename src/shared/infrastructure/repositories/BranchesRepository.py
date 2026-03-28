from typing import List

from src.features.branches.domain.entities.Branch import Branch
from src.features.branches.infrastructure.models.BranchORM import BranchORM
from src.shared.application.Interfaces.IBranchesRepository import IBranchesRepository
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.Decorators.RepositoryDecorator import (
    repo_func,
)


class BranchesRepository(IBranchesRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    @repo_func
    def get_branches(self, session=None) -> List[Branch] | None:
        orm_branches = session.query(BranchORM).all()
        branches = [Branch.model_validate(orm_branch) for orm_branch in orm_branches]
        return branches

    @repo_func
    def add_branch(self, branch: Branch, session=None):
        orm_branch = BranchORM(**branch.model_dump())
        session.add(orm_branch)
        session.commit()

    @repo_func
    def get_branch_by_id(self, id: int, session=None) -> Branch | None:
        branch_orm = session.get(BranchORM, id)

        if branch_orm is None:
            return None

        branch = Branch.model_validate(branch_orm)
        return branch

    @repo_func
    def change_branch_by_id(self, id: int, new_branch: Branch, session=None):
        branch = session.get(BranchORM, id)

        if branch:
            branch.name = new_branch.name
            branch.warehouses = new_branch.warehouses
            session.commit()

    @repo_func
    def delete_branch(self, id: int, session=None):
        branch = session.get(BranchORM, id)
        if branch is not None:
            session.delete(branch)
            session.commit()
