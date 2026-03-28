from abc import ABC, abstractmethod


class IMessageService(ABC):
    @abstractmethod
    def show_success(self, title: str, message: str, parent_widget=None):
        pass

    @abstractmethod
    def show_error(self, title: str, message: str, parent_widget=None):
        pass

    @abstractmethod
    def show_question(self, title: str, message: str, parent_widget=None) -> bool:
        pass
