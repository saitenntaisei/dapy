from dataclasses import dataclass, field
from datetime import timedelta
from typing import Iterable, Self, Any

from ..core import Algorithm, Event, Message, Pid, Signal, System
from .configuration import Configuration
from .timed import TimedConfiguration


@dataclass(frozen=True, order=True)
class LocalTimedEvent:
    """
    Class to represent a send-receive event.
    """
    start: timedelta
    end: timedelta
    event: Event
    
    def is_message(self) -> bool:
        """
        Check if the event is a message.
        """
        return isinstance(self.event, Message)
    
    def is_signal(self) -> bool:
        """
        Check if the event is a signal.
        """
        return isinstance(self.event, Signal)
    
    def sender(self) -> Pid:
        """
        Get the sender of the message.
        """
        return self.event.sender if isinstance(self.event, Message) else self.event.target
    
    def receiver(self) -> Pid:
        """
        Get the receiver of the message.
        """
        return self.event.target


@dataclass
class Trace:
    """
    Class to represent a trace of a simulation.
    """
    system: System
    algorithm_name: str
    
    history: list[TimedConfiguration] = field(default_factory=list)
    events_list: list[LocalTimedEvent] = field(default_factory=list)

    def add_events(self, events: Iterable[tuple[timedelta, timedelta, Event]]) -> None:
        """
        Add events to the trace.
        Message events require two instances: one for the sender time and one for the receiver time.
        """
        self.events_list.extend(LocalTimedEvent(start, end, event) for start, end, event in events)

    def add_history(self, history: Iterable[tuple[timedelta, Configuration]]) -> None:
        """
        Add history to the trace.
        """
        self.history.extend(TimedConfiguration(time, configuration) for time, configuration in history)
