"""
This module contains the core components of the dapy library, which are used to define distributed algorithms and represent distributed executions.
The components are defined in multiple files for better organization and maintainability, but the main ones all re-exported here for convenience.

The core components include:
- `.algorithm`:
    - `.algorithm.Algorithm`: Abstract base class for defining distributed algorithms.
- `.event`:
    - `.event.Event`: Abstract class that represents events in the distributed system, including messages and signals.
        - `.event.Signal`: Abstract subclass that represents signals occurring at some process.
        - `.event.Message`: Abstract subclass that represents messages sent and received between processes.
- `.pid`:
    - `.pid.Pid`: Represents process identifiers (PIDs) in the distributed system.
    - `.pid.ProcessSet`: Represents a set of process identities.
    - `.pid.Channel`: Represents communication channels between processes.
    - `.pid.ChannelSet`: Represents a set of communication channels.
- `.state`:
    - `.state.State`: Abstract class to define the state of a process in the distributed system.
- `.system`:
    - `.system.System`: Represents the distributed system model, including its topology and synchrony model.
    - `.system.SynchronyModel`: Represents the synchrony model of the distributed system, including asynchronous, partially synchronous, and synchronous models.
        - `.system.Synchronous`: Represents a synchronous model for the distributed system.
        - `.system.Asynchronous`: Represents an asynchronous model for the distributed system.
        - `.system.PartiallySynchronous`: Represents a partially synchronous model for the distributed system.
        - `.system.StochasticExponential`: Represents a stochastic exponential model for the distributed system.
- `.topology`:
    - `.topology.NetworkTopology`: Represents the topology of the distributed system, including complete graphs, rings, and stars.
        - `.topology.CompleteGraph`: Represents a complete graph topology for the distributed system.
        - `.topology.Ring`: Represents a ring topology for the distributed system.
        - `.topology.Star`: Represents a star topology for the distributed system.
        - `.topology.ArbitraryGraph`: Represents an arbitrary graph topology for the distributed system, represented by an adjacency list.

This module is essential for defining distributed algorithms, which is done as follows:
```python
from dataclasses import dataclass

# 1. Import the necessary components from the core module.
from dapy.core import Algorithm, Event, Signal, Message, Pid, State

# 2. Define a state of a process by subclassing the State class.
@dataclass(frozen=True)
class MyState(State):
    some_attribute: int = 0
    ...

# 3. Define signal(s) and message(s) by subclassing the relevant class.
@dataclass(frozen=True)
class MySignal(Signal):
    pass
@dataclass(frozen=True)
class MyMessage(Message):
    some_information: str
    
# 4. Define the distributed algorithm by subclassing the Algorithm class and providing an implementation for the two mandatory abstract methods `initial_state` and `on_event`.
@dataclass(frozen=True)
class MyAlgorithm(Algorithm):
    def initial_state(self, pid) -> MyState:
        ...
    def on_event(self, old_state: MyState, event: Event) -> tuple[MyState, list[Event]]:
        ...
```

See the template file and example files for more details on how to define a distributed algorithm using this library.
"""

# re-exports
from .algorithm import Algorithm as Algorithm
from .event import Event as Event
from .event import Message as Message
from .event import Signal as Signal
from .pid import Channel as Channel
from .pid import ChannelSet as ChannelSet
from .pid import Pid as Pid
from .pid import ProcessSet as ProcessSet
from .state import State as State
from .system import Asynchronous as Asynchronous
from .system import PartiallySynchronous as PartiallySynchronous
from .system import StochasticExponential as StochasticExponential
from .system import Synchronous as Synchronous
from .system import SynchronyModel as SynchronyModel
from .system import SynchronyType as SynchronyType
from .system import System as System
from .topology import CompleteGraph as CompleteGraph
from .topology import NetworkTopology as NetworkTopology
from .topology import Ring as Ring
from .topology import Star as Star
