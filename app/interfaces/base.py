from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IModel(ABC):
    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        pass

class IPresenter(ABC):
    @abstractmethod
    def transform_data(self, data: Any) -> Dict[str, Any]:
        pass

class IController(ABC):
    @abstractmethod
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        pass 