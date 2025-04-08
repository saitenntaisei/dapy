"""
This module implements the "Learn the Topology" algorithm, from the .
"""

from dataclasses import dataclass, field
from ..core import Pid, ProcessSet, Channel, ChannelSet, Event, Signal, Message, Algorithm, State


#
# Custom data structure used in the algorithm.
#
@dataclass(frozen=True)
class Position:
    origin: Pid
    neighbors: ProcessSet = field(default_factory=ProcessSet)
    
    def __str__(self) -> str:
        """
        String representation of the position.
        """
        return f"Position({self.origin}, {{{','.join(str(p) for p in sorted(self.neighbors))}}})"


#
# Messages and signals used in the algorithm.
#
@dataclass(frozen=True)
class PositionMsg(Message):
    sender: Pid
    position: Position

@dataclass(frozen=True)
class Start(Signal):
    pass

@dataclass(frozen=True)
class GraphIsKnown(Signal):
    """Event to signal that the graph is known."""
    pass



#
# State of a process in the algorithm.
#
@dataclass(frozen=True)
class LearnState(State):
    own: Position
    known_processes: ProcessSet = field(default_factory=ProcessSet)
    known_channels: ChannelSet = field(default_factory=ChannelSet)
    has_started: bool = False



#
# The algorithm itself.
# 
@dataclass(frozen=True)
class LearnGraphAlgorithm(Algorithm):
    """
    This algorithm learns the topology of the network.
    """
    
    @property
    def name(self) -> str:
        """
        Return the name of the algorithm.
        """
        return "Learn the Topology"
    
    #
    # Mandatory method: given a process id, create and return the initial state of that process.
    #
    def initial_state(self, pid) -> State:
        return LearnState(
            pid=pid,
            own=Position(
                origin=pid,
                neighbors=self.system.topology.neighbors_of(pid)
            ),
            has_started=False,
        )
    
    #
    # Mandatory method:
    # given the state of a process and an event (signal or message) applied to it,
    # return the new state of the process and a list of events to be scheduled.
    #
    def on_event(self, old_state: LearnState, event: Event) -> tuple[LearnState, list[Event]]:
        match event:
            case Start(_) if not old_state.has_started:
                return self._do_start(old_state)
            case Start(_):
                return old_state, []
            case PositionMsg(_, sender, position):
                new_state = old_state
                new_events = []
                # (6) if (not part_i) then start() end if
                if not new_state.has_started:
                    new_state, new_events = self._do_start(new_state)

                # (7) if id not in proc_known_i then                    
                if position.origin not in new_state.known_processes:
                    # (8) proc_known_i := proc_known_i ∪ {id}
                    # (9) channels_known_i := channel_known_i ∪ {<id, id_k> | id_k in neighbors>}
                    # add the new position to the state
                    new_state = new_state.cloned_with(
                        known_processes=new_state.known_processes + position.origin,
                        known_channels=new_state.known_channels + ChannelSet( Channel(position.origin, neighbor) for neighbor in position.neighbors ),
                    )
                    # (10) for each id_y in neighbors_i \ {id_x} do
                    # (11)  send POSITION(id, neighbors) to id_y
                    # (12) end for
                    # send the position to all neighbors except the sender
                    new_events = new_events + [
                        PositionMsg(target=neighbor, sender=old_state.pid, position=position)
                        for neighbor in old_state.own.neighbors
                        if neighbor != sender
                    ]
                    # (13) if forall<id_j, id_k> in channels_known_i : {id_j, id_k} in proc_known_i) then
                    # (14)    p_i knowns the communication graph
                    # (15) end if
                    if all(
                        c_jk.r in new_state.known_processes and c_jk.s in new_state.known_processes
                        for c_jk in new_state.known_channels
                    ):
                        new_events.append(GraphIsKnown(target=new_state.pid))
                    
                # return the new states and all send events
                return new_state, new_events
            case GraphIsKnown(_):
                # Handle the graph known event
                print(f"Graph is known for {old_state.pid}")
                return old_state, []
            case _:
                # Handle other events
                raise NotImplementedError(f"Event {event} not implemented in {self.name}")
            
    #
    # Custom method defined for modularity.
    # Corresponds to the start() method in the pseudo-code of the algorithm.
    #
    def _do_start(self, state: LearnState) -> tuple[LearnState, list[Event]]:
        """
        Handle the start of the algorithm.
        """
        # Send a message to all neighbors with the current position
        events = [
            PositionMsg(target=neighbor, sender=state.own.origin, position=state.own)
            for neighbor in state.own.neighbors
        ]
        state = state.cloned_with(
            known_processes=ProcessSet(state.own.origin),
            known_channels=ChannelSet( Channel(state.own.origin, neighbor) for neighbor in state.own.neighbors ),
            has_started=True,
        )
        return state, events

