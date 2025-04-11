from dataclasses import dataclass
from typing import Iterable, Self

from ..core import Pid, State


@dataclass(frozen=True)
class Configuration:
    states: dict[Pid, State]

    def updated(self, states: Iterable[State]) -> Self:
        """
        Create a new configuration with updated states.
        """
        new_states = {state.pid: state for state in states}
        updated_states = {pid: new_states.get(pid, state) for pid, state in self.states.items()}
        return Configuration(updated_states)

    def processes(self) -> Iterable[Pid]:
        """
        Get the PIDs of all processes in the configuration.
        """
        return sorted(self.states.keys())
    
    def changed_from(self, other: Self) -> Iterable[Pid]:
        """
        Get the PIDs of processes that have changed between two configurations.
        """
        return (pid for pid in self.processes() if pid in other and self.states[pid] != other.states[pid])
    
    def __getitem__(self, pid: Pid) -> State:
        """
        Get the state of a process by its PID.
        """
        return self.states.get(pid)

    def __contains__(self, pid: Pid) -> bool:
        """
        Check if a process is in the configuration.
        """
        return pid in self.states

    def __iter__(self) -> Iterable[State]:
        """
        Iterate over the states in the configuration.
        """
        return iter(self.states.values())
    
    def __len__(self) -> int:
        """
        Get the number of states in the configuration.
        """
        return len(self.states)

    @classmethod
    def from_states(cls, states: Iterable[State]) -> Self:
        """
        Create a configuration from a list of states.
        """
        return cls(states={state.pid: state for state in states})

    def __str__(self) -> str:
        """
        String representation of the configuration.
        """
        states = '\n  '.join(str(self.states[p]) for p in sorted(self.states.keys()) )
        return f"Configuration:\n  {states if states else '<empty>'}"
