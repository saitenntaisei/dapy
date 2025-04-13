from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Iterable, Self

import classifiedjson

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

    def dumps(self) -> str:
        """
        Serialize the trace to a string.
        """
        return classifiedjson.dumps(self, custom_hooks=[_timedelta_serialize])

    @classmethod
    def loads(cls, data: str) -> Self:
        """
        Deserialize the trace from a string.
        """
        return classifiedjson.loads(data, custom_hooks=[_timedelta_deserialize])


import re

from classifiedjson import Factory, is_exact_match


def _parse_timedelta(timedelta_str: str) -> timedelta:
    """
    Parse a string to create a timedelta object.
    """
    match = re.match(r"^datetime.timedelta\((?P<args>.*)\)$", timedelta_str)
    if not match:
        raise ValueError(f"Invalid timedelta string: {timedelta_str}")
    
    args = match.group("args").split(",")
    kwargs = {}
    if args == ["0"]:
        return timedelta(0)
    
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=")
            kwargs[key.strip()] = eval(value.strip())
        else:
            kwargs[arg.strip()] = None
    
    return timedelta(**kwargs)


def _timedelta_serialize(obj: timedelta) -> str:
    """
    Serialize a timedelta object to a string.
    """
    if not is_exact_match(obj, timedelta):
        return NotImplemented
    return repr(obj)

def _timedelta_deserialize(factory: Factory, obj: str) -> timedelta:
    """
    Deserialize a string to a timedelta object.
    """
    if not factory.is_exact_match(timedelta):
        return NotImplemented
    return _parse_timedelta(obj)

shitcspell = 0
"""shitcspell is real shit"""
