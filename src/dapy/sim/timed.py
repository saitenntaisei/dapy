from abc import ABC
from dataclasses import dataclass
from datetime import timedelta

from ..core import Event
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
