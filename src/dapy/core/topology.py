from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Iterable
from .pid import Pid


@dataclass(frozen=True)
class NetworkTopology(ABC):
    """
    Abstract class to represent a network topology.
    """
    @abstractmethod
    def neighbors_of(self, ) -> frozenset[Pid]:
        """
        Given a process identifier (PID), return its neighbors.
        """
        pass
    
    @abstractmethod
    def processes(self) -> frozenset[Pid]:
        """
        Return the set of processes in the topology.
        """
        pass


@dataclass(frozen=True)
class CompleteGraph(NetworkTopology):
    _processes: frozenset[Pid]
    
    def neighbors_of(self, pid: Pid) -> frozenset[Pid]:
        return self._processes - {pid}

    def processes(self) -> frozenset[Pid]:
        return self._processes
    
    @classmethod
    def from_(cls, processes: Iterable[Pid]) -> 'CompleteGraph':
        return cls(frozenset(processes))
    
    @classmethod
    def of_size(cls, size: int) -> 'CompleteGraph':
        """
        Create a complete graph topology with the given size.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        return cls.from_(Pid(i+1) for i in range(size))


@dataclass(frozen=True)
class Ring(NetworkTopology):
    _processes: list[Pid] = field()
    _index: dict[Pid, int] = field()
    directed: bool = field(default=False)
    
    def neighbors_of(self, pid: Pid) -> frozenset[Pid]:
        idx = self._index.get(pid)
        if idx is None:
            raise ValueError(f"Process {pid} not found in the ring topology.")
        if self.directed:
            return frozenset({self._processes[(idx + 1) % len(self._processes)]})
        return frozenset({self._processes[(idx - 1)], 
                          self._processes[(idx + 1) % len(self._processes)]})

    def processes(self) -> frozenset[Pid]:
        return frozenset(self._processes)
    
    @classmethod
    def from_(cls, processes: Iterable[Pid], directed: bool = False) -> 'Ring':
        processes = sorted(set(processes))
        index = {pid: i for i, pid in enumerate(processes)}
        return cls(processes, index, directed)
    
    @classmethod
    def of_size(cls, size: int, directed: bool = False) -> 'Ring':
        """
        Create a ring topology with the given size.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        return cls.from_((Pid(i+1) for i in range(size)), directed=directed)


if __name__ == "__main__":
    # Example usage
    topology = Ring.from_({Pid(1), Pid(2), Pid(3)}, directed=True)
    print(topology.neighbors_of(Pid(1)))
    print(topology.processes())
    print(topology.neighbors_of(Pid(3)))
