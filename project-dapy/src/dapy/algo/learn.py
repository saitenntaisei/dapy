from dataclasses import dataclass, field
from ..core import Pid, ProcessSet, Channel, ChannelSet, Event, Signal, Message, Algorithm, State


@dataclass(frozen=True)
class Position:
    origin: Pid
    neighbors: ProcessSet = field(default_factory=ProcessSet)
    
    def __str__(self) -> str:
        """
        String representation of the position.
        """
        return f"Position({self.origin}, {{{','.join(str(p) for p in sorted(self.neighbors))}}})"
    
@dataclass(frozen=True)
class PositionMsg(Message):
    sender: Pid
    position: Position

@dataclass(frozen=True)
class Start(Signal):
    pass



@dataclass(frozen=True)
class LearnState(State):
    own: Position
    known_processes: ProcessSet = field(default_factory=ProcessSet)
    known_channels: ChannelSet = field(default_factory=ChannelSet)
    has_started: bool = False

        
@dataclass(frozen=True)
class LearnGraphAlgorithm(Algorithm):
    """
    This algorithm learns the topology of the network.
    """
    
    def initial_state(self, pid) -> State:
        return LearnState(
            pid=pid,
            own=Position(
                origin=pid,
                neighbors=self.system.topology.neighbors_of(pid)
            ),
            has_started=False,
        )
    
    def on_event(self, old_state: LearnState, event: Event) -> tuple[LearnState, list[Event]]:
        match event:
            case Start(_) if not old_state.has_started:
                return self._do_start(old_state)
            case Start(_):
                return old_state, []
            case PositionMsg(_, _, position) if position.origin in old_state.known_processes:
                return old_state, []
            case PositionMsg(_, sender, position):
                new_state = old_state
                new_events = []
                # start the process if it has not started yet
                if not new_state.has_started:
                    new_state, new_events = self._do_start(new_state)
                # add the new position to the state
                new_state = new_state.copy(
                    known_processes=new_state.known_processes + position.origin,
                    known_channels=new_state.known_channels + ChannelSet( Channel(position.origin, neighbor) for neighbor in position.neighbors ),
                )
                # send the position to all neighbors except the sender
                new_events = new_events + [
                    PositionMsg(target=neighbor, sender=old_state.pid, position=position)
                    for neighbor in old_state.own.neighbors
                    if neighbor != sender
                ]
                return new_state, new_events
            case _:
                # Handle other events
                raise NotImplementedError(f"Event {event} not implemented in {self.name}")
            
    def _do_start(self, state: LearnState) -> tuple[LearnState, list[Event]]:
        """
        Handle the start of the algorithm.
        """
        # Send a message to all neighbors with the current position
        events = [
            PositionMsg(target=neighbor, sender=state.own.origin, position=state.own)
            for neighbor in state.own.neighbors
        ]
        state = state.copy(
            known_processes=ProcessSet(state.own.origin),
            known_channels=ChannelSet( Channel(state.own.origin, neighbor) for neighbor in state.own.neighbors ),
            has_started=True,
        )
        return state, events

