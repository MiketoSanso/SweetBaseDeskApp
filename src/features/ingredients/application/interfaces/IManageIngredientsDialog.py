from abc import ABC, abstractmethod
from typing import Callable


class IManageIngredientsDialog(ABC):

    @abstractmethod
    def set_mode_management(self):
        pass

    @abstractmethod
    def set_mode_selection(self):
        pass

    @abstractmethod
    def set_on_ingredient_selected(self, callback: Callable[[int, int], None]):
        pass

    @abstractmethod
    def set_on_add_ingredient_requested(self, callback: Callable[[], None]):
        pass

    @abstractmethod
    def set_on_edit_ingredient_requested(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def set_on_delete_ingredient_requested(self, callback: Callable[[int], None]):
        pass

    @abstractmethod
    def display_ingredients(self, ingredients, has_ingredients):
        pass

    @abstractmethod
    def close_dialog(self):
        pass
