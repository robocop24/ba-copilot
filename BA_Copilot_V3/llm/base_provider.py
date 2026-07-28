from abc import ABC
from abc import abstractmethod

class BaseProvider(ABC):
    
    @abstractmethod
    def get_llm(self):
        pass