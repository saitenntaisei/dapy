from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .pid import Pid
from .system import SynchronyModel, System
from .event import Event
from typing import Self, Iterable, Optional


@dataclass(frozen=True)
class State(ABC):
    """
    Abstract class to represent the state of an algorithm.
    """
    pid: Pid
    
    def copy(self, **kwargs) -> Self:
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
    

@dataclass(frozen=True)
class Algorithm(ABC):
    """
    Abstract class to represent an algorithm in the system.
    """
    system: System

    def name(self) -> str:
        """
        Return the name of the algorithm.
        """
        return type(self).__name__
    
    @abstractmethod
    def initial_state(self, pid: Pid) -> State:
        """
        Initialize the algorithm with the given system.
        """
        pass
    
    def on_start(self, init_state: State) -> tuple[State, list[Event]]:
        """
        Handle the start of the algorithm.
        """
        return init_state, []
    
    @abstractmethod
    def on_event(self, old_state: State, event: Event) -> tuple[State, list[Event]]:
        """
        Handle an event.
        Given the old state and the event, return the new state and a list of events to be sent.
        """
        pass

