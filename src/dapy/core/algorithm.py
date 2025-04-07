from dataclasses import dataclass
from abc import ABC, abstractmethod
from .pid import Pid
from .system import System
from .event import Event
from .state import State


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

