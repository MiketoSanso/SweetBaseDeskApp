import functools
import logging
from typing import Callable, TypeVar

from src.shared.application.dtos.ProcessDTO import ProcessDTO

T = TypeVar("T")


def usecase_func(func: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(self.__class__.__name__)
            logger.exception(f"Exception in {func.__name__}")
            return ProcessDTO(
                status=False, message="Ошибка при выполнении операции", error=str(e)
            )

    return wrapper
