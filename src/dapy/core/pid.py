from dataclasses import dataclass, field
from typing import Iterable, Self


@dataclass(frozen=True, order=True)
class Pid:
    """
    Class to represent a process identifier (PID).
    
    Attributes:
        id (int): The unique identifier for the process.
    """
    id: int
    
    def __str__(self) -> str:
        return f"p{self.id}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"


@dataclass(frozen=True)
class ProcessSet:
    """
    Class to represent a set of processes.
    
    Attributes:
        processes (frozenset[Pid]): A set of unique process identifiers.
    """
    processes: frozenset[Pid] = field(default_factory=frozenset)
    
    def __init__(self, processes: Iterable[Pid] | Pid = frozenset()):
        if isinstance(processes, Pid):
            processes = {processes}
        object.__setattr__(self, 'processes', frozenset(processes))
        
    def __str__(self) -> str:
        return f"{{{','.join(str(p) for p in sorted(self.processes))}}}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({{{','.join(repr(p) for p in sorted(self.processes))}}})"
    
    def __contains__(self, pid: Pid) -> bool:
        return pid in self.processes
    
    def __len__(self) -> int:
        return len(self.processes)
    
    def __iter__(self) -> Iterable[Pid]:
        return iter(self.processes)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ProcessSet):
            return False
        return self.processes == other.processes
    
    def __add__(self, other) -> Self:
        if isinstance(other, Pid):
            return ProcessSet(processes=self.processes.union({other}))
        elif isinstance(other, ProcessSet):
            return ProcessSet(processes=self.processes.union(other.processes))
        elif isinstance(other, Iterable):
            return ProcessSet(processes=self.processes.union(other))
        else:
            raise TypeError("Cannot join ProcessSet with non-ProcessSet object")
        
    @staticmethod
    def empty() -> Self:
        """
        Return an empty ProcessSet.
        """
        return ProcessSet()


@dataclass(frozen=True, order=True)
class Channel:
    """
    Class to represent a communication channel between two processes.
    
    By default, channels are directed, in the sense that `s` is a sender process and `r` is a receiver process.
    If you want to create an undirected channel, set the `directed` parameter to False.
    In this case, the order of the processes does not matter for equality or comparison.
    
    Attributes:
        s (Pid): The sender process identifier.
        r (Pid): The receiver process identifier.
        directed (bool): Indicates if the channel is directed or not. Default is True.
    """
    s: Pid
    r: Pid
    directed: bool = True
    
    def __str__(self) -> str:
        return f"<{self.s.id},{self.r.id}>"
    
    def __repr__(self) -> str:
        if self.directed:
            return f"{self.__class__.__name__}({repr(self.s)},{repr(self.r)})"
        return f"{self.__class__.__name__}({repr(self.s)},{repr(self.r)}, directed=False)"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Channel):
            return False
        if self.directed and other.directed:
            return self.as_tuple() == other.as_tuple()
        else:
            return self.normalized() == other.normalized()
        
    def __cmp__(self, other) -> int:
        if not isinstance(other, Channel):
            raise TypeError("Cannot compare Channel with non-Channel object")
        if self.directed and other.directed:
            a = self.as_tuple()
            b = other.as_tuple()
        else:
            a = self.normalized()
            b = other.normalized()
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
        
    def __hash__(self) -> int:
        if self.directed:
            return hash(self.as_tuple())
        else:
            return hash(self.normalized())
    
    def as_tuple(self) -> tuple[Pid, Pid]:
        """
        Return the channel as a tuple of PIDs.
        """
        return (self.s, self.r)
        
    def normalized(self) -> tuple[Pid, Pid]:
        """
        Return a normalized representation of the channel, where `s` <= `r`.
        """
        if self.s <= self.r:
            return (self.s, self.r)
        else:
            return (self.r, self.s)


@dataclass(frozen=True)
class ChannelSet:
    """
    Class to represent a set of channels.
    
    Attributes:
        channels (frozenset[Channel]): A set of unique channels.
    """
    channels: frozenset[Channel] = field(init=False)
    
    def __init__(self, channels: Iterable[Channel] | Channel = frozenset()):
        if isinstance(channels, Channel):
            channels = {channels}
        object.__setattr__(self, 'channels', frozenset(channels))
        
    def __str__(self) -> str:
        return f"{{{','.join(str(c) for c in sorted(self.channels))}}}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({{{','.join(repr(c) for c in sorted(self.channels))}}})"
    
    def __contains__(self, channel: Channel) -> bool:
        return channel in self.channels
    
    def __len__(self) -> int:
        return len(self.channels)
    
    def __iter__(self) -> Iterable[Channel]:
        return iter(self.channels)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ChannelSet):
            return False
        return self.channels == other.channels
    
    def __add__(self, other) -> Self:
        if isinstance(other, Channel):
            return ChannelSet(channels=self.channels.union({other}))
        elif isinstance(other, ChannelSet):
            return ChannelSet(channels=self.channels.union(other.channels))
        elif isinstance(other, Iterable):
            return ChannelSet(channels=self.channels.union(other))
        else:
            raise TypeError("Cannot join ChannelSet with non-ChannelSet object")

