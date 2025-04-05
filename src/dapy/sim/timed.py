from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import timedelta

from ..core.event import Event
from .configuration import Configuration


@dataclass(frozen=True, order=True)
class Timed(ABC):
    """
    Abstract base class to represent a timed object.
    """
    time: timedelta


@dataclass(frozen=True, order=True)
class TimedEvent(Timed):
    """
    Class to represent a timed event.
    """
    event: Event


@dataclass(frozen=True, order=True)
class TimedConfiguration(Timed):
    """
    Class to represent a timed configuration.
    """
    configuration: Configuration
