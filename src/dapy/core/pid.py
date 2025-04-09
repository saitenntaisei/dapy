from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True, order=True)
class Pid:
    """
    Class to represent a process identifier (PID).
    """
    id: int
    
    def __str__(self):
        return f"p{self.id}"


@dataclass(frozen=True)
class ProcessSet:
    """
    Class to represent a set of processes.
    """
    processes: frozenset[Pid] = field(default_factory=frozenset)
    
    def __init__(self, processes: Iterable[Pid] | Pid = frozenset()):
        if isinstance(processes, Pid):
            processes = {processes}
        object.__setattr__(self, 'processes', frozenset(processes))
    def __str__(self):
        return f"{{{','.join(str(p) for p in sorted(self.processes))}}}"
    def __contains__(self, pid: Pid) -> bool:
        return pid in self.processes
    def __len__(self) -> int:
        return len(self.processes)
    def __iter__(self):
        return iter(self.processes)
    def __eq__(self, other):
        if not isinstance(other, ProcessSet):
            return False
        return self.processes == other.processes
    def __add__(self, other):
        if isinstance(other, Pid):
            return ProcessSet(processes=self.processes.union({other}))
        elif isinstance(other, ProcessSet):
            return ProcessSet(processes=self.processes.union(other.processes))
        elif isinstance(other, Iterable):
            return ProcessSet(processes=self.processes.union(other))
        else:
            raise TypeError("Cannot join ProcessSet with non-ProcessSet object")


@dataclass(frozen=True, order=True)
class Channel:
    """
    Class to represent a communication channel between two processes.
    """
    s: Pid
    r: Pid
    directed: bool = True
    
    def __str__(self):
        return f"<{self.s.id},{self.r.id}>"
    
    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        if self.directed and other.directed:
            return self.s == other.s and self.r == other.r
        else:
            return self.normalized() == other.normalized()
        
    def __cmp__(self, other) -> int:
        if not isinstance(other, Channel):
            raise TypeError("Cannot compare Channel with non-Channel object")
        if self.directed and other.directed:
            a = (self.s, self.r)
            b = (other.s, other.r)
        else:
            a = self.normalized()
            b = other.normalized()
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
        
    def __hash__(self):
        if self.directed:
            return hash((self.s, self.r))
        else:
            return hash(self.normalized())
    
    def as_tuple(self) -> tuple[Pid, Pid]:
        """
        Return the channel as a tuple of PIDs.
        """
        return (self.s, self.r)
        
    def normalized(self) -> tuple[Pid, Pid]:
        """
        Return a normalized representation of the channel.
        """
        if self.s < self.r:
            return (self.s, self.r)
        else:
            return (self.r, self.s)


@dataclass(frozen=True)
class ChannelSet:
    """
    Class to represent a set of channels.
    """
    channels: frozenset[Channel] = field(init=False)
    
    def __init__(self, channels: Iterable[Channel] | Channel = frozenset()):
        if isinstance(channels, Channel):
            channels = {channels}
        object.__setattr__(self, 'channels', frozenset(channels))
    def __str__(self):
        return f"{{{','.join(str(c) for c in sorted(self.channels))}}}"
    def __contains__(self, channel: Channel) -> bool:
        return channel in self.channels
    def __len__(self) -> int:
        return len(self.channels)
    def __iter__(self):
        return iter(self.channels)
    def __eq__(self, other):
        if not isinstance(other, ChannelSet):
            return False
        return self.channels == other.channels
    def __add__(self, other):
        if isinstance(other, Channel):
            return ChannelSet(channels=self.channels.union({other}))
        elif isinstance(other, ChannelSet):
            return ChannelSet(channels=self.channels.union(other.channels))
        elif isinstance(other, Iterable):
            return ChannelSet(channels=self.channels.union(other))
        else:
            raise TypeError("Cannot join ChannelSet with non-ChannelSet object")
