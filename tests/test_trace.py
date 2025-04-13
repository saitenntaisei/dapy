import pytest
import re
import classifiedjson
from classifiedjson import is_exact_match, Factory

from dapy.core import Pid, System, Ring, Synchronous
from dapy.algo.learn import LearnGraphAlgorithm, Start
from dapy.sim import Simulator, Settings, Trace
from datetime import timedelta


def parse_timedelta(timedelta_str: str) -> timedelta:
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


def timedelta_serialize(obj: timedelta) -> str:
    """
    Serialize a timedelta object to a string.
    """
    if not is_exact_match(obj, timedelta):
        return NotImplemented
    return repr(obj)

def timedelta_deserialize(factory: Factory, obj: str) -> timedelta:
    """
    Deserialize a string to a timedelta object.
    """
    if not factory.is_exact_match(timedelta):
        return NotImplemented
    return parse_timedelta(obj)



def test_trace_generation():
    settings = Settings(enable_trace=True)
    
    # define system, algorithm and simulator
    system = System(
        topology=Ring.of_size(3),
        synchrony=Synchronous(fixed_delay=timedelta(seconds=1)),
    )
    algorithm = LearnGraphAlgorithm(system)
    sim = Simulator.from_system(system, algorithm, settings=settings)

    # run the simulation
    sim.start()
    sim.schedule_event(timedelta(seconds=0), Start(target=Pid(1)))
    sim.run_to_completion()

    # analyze the trace
    assert sim.trace.system == system
    assert sim.trace.algorithm_name == algorithm.name
    assert len(sim.trace.history) == 16
    assert len(sim.trace.events_list) == 16
    assert len(sim.trace.history[0].configuration) == 3
    assert sim.trace.history[0].time == timedelta(seconds=0)
    assert sim.trace.history[-1].configuration == sim.current_configuration
    assert sim.trace.history[-1].time == sim.current_time
    assert sim.current_time == timedelta(seconds=3)

    trace_json = sim.trace.dumps()
    trace2 = Trace.loads(trace_json)
    assert trace2 == sim.trace

if __name__ == "__main__":
    test_trace_generation()
