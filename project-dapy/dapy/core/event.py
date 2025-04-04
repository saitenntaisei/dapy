from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .pid import Pid

@dataclass(frozen=True)
class Event(ABC):
    """
    Abstract class to represent an event in the system.
    """
    target: Pid

@dataclass(frozen=True)
class Signal(Event):
    """
    Class to represent a signal event.
    """

@dataclass(frozen=True)
class Message(Event):
    """
    Class to represent a receive event.
    """
    sender: Pid



if __name__ == "__main__":
    @dataclass(frozen=True, eq=True)
    class Pos:
        origin: Pid
        neighbors: frozenset[Pid] = field(default_factory=frozenset)
    
    # Example usage
    @dataclass(frozen=True)
    class Start(Signal):
        pass

    @dataclass(frozen=True)
    class Position(Message):
        pos: Pos



    s = Start(target=Pid(1))
    print(s)
    print(s.target)

    p = Position(target=Pid(1), sender=Pid(2), pos=Pos(Pid(1), frozenset({Pid(2), Pid(3)})))
    print(p)
    print(p.target)
    print(p.sender)
