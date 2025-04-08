from dapy.core import Pid, System, Ring, Asynchronous
from dapy.algo.learn import LearnGraphAlgorithm, Start
from dapy.sim import Simulator, Settings
from datetime import timedelta


# Example usage
settings = Settings(enable_trace=True)

system = System(
    topology=Ring.of_size(4),
    synchrony=Asynchronous(),
)
print("System:")
print(system)

algorithm = LearnGraphAlgorithm(system)
print("Algorithm:", algorithm.name)
print(algorithm)

sim = Simulator.from_system(system, algorithm, settings=settings)
sim.start()
sim.schedule_event(timedelta(seconds=0), Start(target=Pid(1)))
sim.run_to_completion()

print('\n' * 5)

print("----[ Trace ]---- configuration history")
for event in sim.trace.history:
    time = event.time
    event = event.configuration
    print(f"{time} {event}")
print("----[ Trace ]---- ")
for timed_event in sim.trace.events_list:
    start = timed_event.start
    end = timed_event.end
    event = timed_event.event
    print(f"{start} {end} {event}")

for i in range(len(sim.trace.history)-1):
    for p in sim.trace.history[i+1].configuration.changed_from(sim.trace.history[i].configuration):
        print(f"+++ Process {p} changed from config {i} to {i+1}")
