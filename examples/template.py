from dataclasses import dataclass

from dapy.core import Algorithm, Event, Message, Signal, State

#
# Define the State of a process in the algorithm.
#

@dataclass(frozen=True)
class MyState(State):
    # inherited from State
    #   pid: Pid
    # declare any other relevant fields
    ...

#
# Define the messages and signals used in the algorithm.
#

@dataclass(frozen=True)
class MyMessage(Message):
    # inherited from Message
    #   target: Pid
    #   sender: Pid
    # declare any other relevant fields
    ...
    
@dataclass(frozen=True)
class MySignal(Signal):
    # inherited from Signal
    #   target: Pid
    # declare any other relevant fields
    ...
    
#
# Define the algorithm itself.
#
@dataclass(frozen=True)
class MyAlgorithm(Algorithm):
    """
    This algorithm does something.
    """
    # inherited from Algorithm
    #   system: System
    
    #
    # Mandatory method: given a process id, create and return the initial state of that process.
    #
    def initial_state(self, pid) -> MyState:
        """
        Create and return the initial state of the process.
        """
        return MyState(
            pid=pid,
            # initialize any other relevant fields
            # ...
        )
    
    #
    # Mandatory method:
    # given the state of a process and an event (signal or message) applied to it,
    # return the new state of the process and a list of events to be scheduled.
    #
    def on_event(self, old_state: MyState, event: Event) -> tuple[MyState, list[Event]]:
        """
        Given the state of a process and an event, return the new state and a list of events to be scheduled.
        """
        # implement the algorithm logic here
        ...
        new_state = old_state.cloned_with(...)
        new_events = [...]
        ...
        return new_state, new_events

    #
    # Optional methods
    #
    
    @property
    def name(self) -> str:
        """
        Return the name of the algorithm.
        """
        return "My Algorithm"
    
    def on_start(self, init_state):
        """
        Given the initial state of a process, return a modified state and a list of events to be scheduled.
        """
        # Although the the state can be modified, the intention is mainly to provide a way to issue initial events.
        # This is not always needed, as the initial events can also be scheduled externally.
        return init_state, [...]



if __name__ == "__main__":
    #
    # Algorithm execution
    #

    from dapy.core import System  # ...
    from dapy.sim import Settings, Simulator

    #
    # optionally define settings (e.g. enable trace)
    #
    settings = Settings(enable_trace=True)

    #
    # define the system (topology, synchrony model)
    #
    system = System(
        topology= ...,
        synchrony= ...,
    )

    #
    # Instantiate the algorithm
    #
    algorithm = MyAlgorithm(system)

    #
    # Create the simulator environment
    #
    sim = Simulator.from_system(system, algorithm, settings=settings)

    #
    # Run the simulation
    #
    
    # Start the simulation; all processes are initialized to their initial state 
    sim.start()
    # Possibly schedule some initial event(s)
    sim.schedule_event(...)
    # Run the algorithm until completion
    sim.run_to_completion()

    #
    # Check the final state of the system
    #
    print(sim.current_time) # final time reached by the simulation
    print(sim.current_configuration) # final configuration of the system
    print(sim.trace) # trace of the simulation (if enabled)
