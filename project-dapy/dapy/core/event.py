from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .pid import Pid

@dataclass(frozen=True, order=True)
class Event(ABC):
    """
    Abstract class to represent an event in the system.
    """
    target: Pid
    
    def __str__(self) -> str:
        """
        String representation of the start signal.
        """
        other_attributes = ', '.join(f"{k}={str(v)}" for k,v in self.__dict__.items() if k != 'target' and v is not None)
        if other_attributes:
            other_attributes = "; " + other_attributes
        return f"{self.__class__.__name__}(@{self.target}{other_attributes})"
        

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
