from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional
import heapq

from ..core import System, Algorithm, Event, Message
from .configuration import Configuration
from .timed import TimedEvent 
from .settings import Settings
from .trace import Trace


@dataclass
class Simulator:
    system: System
    algorithm: Algorithm
    current_configuration: Configuration
    current_time: timedelta = field(default=timedelta(seconds=0))
    settings: Settings = field(default_factory=Settings)
    trace: Optional[Trace] = field(default=None)
    scheduled_events: list[TimedEvent] = field(default_factory=list, init=False)
    
    
    def __post_init__(self):
        """
        Initialize the simulator with the given settings.
        """
        if self.settings.enable_trace:
            self.trace = Trace(system=self.system, algorithm=self.algorithm)
    
    @classmethod
    def from_system(cls, system: System, algorithm: Algorithm, starting_time: timedelta = timedelta(seconds=0), settings: Settings = Settings()) -> "Simulator":
        """
        Create a simulator instance from the given system and algorithm.
        """
        current_configuration = Configuration.from_states( algorithm.initial_state(p) for p in system.processes())
        return cls(system=system, algorithm=algorithm, current_configuration=current_configuration, current_time=starting_time, settings=settings)       
    
    def start(self) -> None:
        """
        Start the simulation.
        """
        self.current_time = timedelta(seconds=0)
        for pid in self.system.processes():
            initial_state, events = self.algorithm.on_start(self.current_configuration[pid])
            self.current_configuration = self.current_configuration.updated([initial_state])
            for event in events:
                at_time = self._arrival_time_for(event)
                self.schedule_event(at_time, event)
    
    def _arrival_time_for(self, event: Event) -> timedelta:
        """
        Calculate the delay for a given event.
        """
        if isinstance(event, Message):
            return self.system.synchrony.arrival_time_for(self.current_time)
        else:
            return self.current_time
        
    def schedule_event(self, at: timedelta, event: Event) -> None:
        """
        Schedule an event to be processed at a specific time.
        """
        time = max(self.current_time, at)
        heapq.heappush(self.scheduled_events, TimedEvent(time=time, event=event))
        if self.trace is not None:
            self.trace.add_events([(self.current_time, time, event)])

    def _apply_event(self, event: Event) -> None:
        """
        Apply an event to the current configuration.
        """
        pid = event.target
        if pid not in self.current_configuration:
            raise ValueError(f"{pid} not found in the current configuration.")
        old_state = self.current_configuration[pid]
        new_state, new_events = self.algorithm.on_event(old_state, event)
        self.current_configuration = self.current_configuration.updated([new_state])
        for new_event in new_events:
            at_time = self._arrival_time_for(new_event)
            self.schedule_event(at_time, new_event)
        
    def advance_step(self) -> None:
        """
        Advance the simulation by one step.
        """
        if len(self.scheduled_events) > 0:
            next_event = heapq.heappop(self.scheduled_events)
            self.current_time = max(self.current_time, next_event.time)
            self._apply_event(next_event.event)
            if self.trace is not None:
                self.trace.add_history([(self.current_time, self.current_configuration)])

    def run_to_completion(self, step_limit: Optional[int] = None) -> None:
        """
        Run the simulation until it is finished or until an optional step limit is reached.
        """
        step_count = 0
        while not self.is_finished() and (step_limit is None or step_count < step_limit):
            self.advance_step()
            step_count += 1

    def is_finished(self) -> bool:
        """
        Check if the simulation has finished.
        """
        return len(self.scheduled_events) == 0

    def __str__(self) -> str:
        """
        String representation of the simulator.
        """
        scheduled = '\n'.join( f"  {timed_event.time}: {timed_event.event}" for timed_event in self.scheduled_events )
        return f"""Simulator ({self.algorithm.name()}) @{self.current_time}:
{self.current_configuration}
Scheduled Events:
{scheduled}"""
