import functools
from typing import Callable, TypeVar

T = TypeVar("T")


def repo_func(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        session = self.db.get_session()
        try:
            result = func(self, *args, **kwargs, session=session)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper
