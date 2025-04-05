from dataclasses import dataclass
from typing import Iterable

from ..core.algorithm import State
from ..core.pid import Pid


@dataclass(frozen=True)
class Configuration:
    states: dict[Pid, State]

    def updated(self, states: Iterable[State]) -> 'Configuration':
        """
        Create a new configuration with updated states.
        """
        new_states = {state.pid: state for state in states}
        updated_states = {pid: new_states.get(pid, state) for pid, state in self.states.items()}
        return Configuration(updated_states)

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

    def __iter__(self):
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
    def from_states(cls, states: Iterable[State]) -> 'Configuration':
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
