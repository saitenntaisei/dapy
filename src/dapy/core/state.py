from dataclasses import dataclass
from abc import ABC
from typing import Self, Iterable, Optional
from .pid import Pid


@dataclass(frozen=True)
class State(ABC):
    """
    Abstract class to represent the state of an algorithm.
    """
    pid: Pid
    
    def cloned_with(self, **kwargs) -> Self:
        """
        Create a copy of the state with updated attributes.
        """
        return self.__class__(**{**self.__dict__, **kwargs})
    
    def as_str(self, keys: Optional[Iterable[str]] = None) -> str:
        """
        String representation of the state.
        """
        keys = self.__dict__.keys() if keys is None else keys
        return f"{self.pid}: " + ", ".join(f"{k}={str(self.__dict__.get(k))}" for k in keys if k != "pid")
    
    def __str__(self) -> str:
        """
        String representation of the state.
        """
        return self.as_str()
