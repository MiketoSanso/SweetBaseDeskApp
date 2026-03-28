from abc import ABC, abstractmethod


class IMainWindow(ABC):
    @property
    @abstractmethod
    def catalog_tab(self):
        pass

    @property
    @abstractmethod
    def transaction_tab(self):
        pass

    @property
    @abstractmethod
    def ingredients_tab(self):
        pass

    @property
    @abstractmethod
    def branches_tab(self):
        pass

    @property
    @abstractmethod
    def stock_tab(self):
        pass

    @property
    @abstractmethod
    def reports_tab(self):
        pass
