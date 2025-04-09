import pytest
from typing import Optional

from dapy.core.topology import Pid, ProcessSet, Channel, NetworkTopology, CompleteGraph, Ring, Star, Arbitrary

def _all_processes_are_present(topology: NetworkTopology, processes: ProcessSet):
    """
    Check that all processes are present in the topology.
    """
    for pid in processes:
        assert pid in topology.processes()
        assert pid in topology
        
def _no_process_is_its_own_neighbor(topology: NetworkTopology):
    """
    Check that no process is its own neighbor in the topology.
    """
    for pid in topology:
        assert pid not in topology.neighbors_of(pid)

def _check_any_topology(topology: NetworkTopology, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    assert topology.processes() == processes
    assert len(topology) == size
    assert len(topology.processes()) == size
    assert Pid(min(processes).id-1) not in topology
    assert min(processes) in topology
    assert max(processes) in topology
    assert Pid(max(processes).id+1) not in topology
    _all_processes_are_present(topology, processes)
    _no_process_is_its_own_neighbor(topology)
    
def _check_ring_validity(topology: Ring, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    
    indexed_processes = list(processes)
    
    # Check the neighbors of each process
    for i, pid in enumerate(processes):
        prev = indexed_processes[i-1]
        next = indexed_processes[(i+1)%size]
        assert len(topology.neighbors_of(pid)) == 2
        assert topology.neighbors_of(pid) == ProcessSet({prev, next})

def _check_complete_graph_validity(topology: CompleteGraph, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    # Check the neighbors of each process
    for pid in processes:
        assert len(topology.neighbors_of(pid)) == size - 1
        assert topology.neighbors_of(pid) + {pid} == topology.processes()

def _check_star_validity(topology: Star, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    # Check the neighbors of each process
    for pid in processes:
        if pid == topology.center():
            assert len(topology.neighbors_of(pid)) == size - 1
            assert topology.neighbors_of(pid) + {pid} == topology.processes()
        else:
            assert len(topology.neighbors_of(pid)) == 1
            assert topology.neighbors_of(pid) == ProcessSet(topology.center())

def test_ring():
    """
    Test the Ring topology.
    """
    for size in [2, 4, 9]:
        size = 4
        # Create a ring topology with 4 processes
        topology = Ring.of_size(size)
        _check_any_topology(topology, size)
        _check_ring_validity(topology, size)
    
    processes = ProcessSet({Pid(10), Pid(20), Pid(30)})
    topology = Ring.from_(processes)
    _check_any_topology(topology, 3, processes)
    _check_ring_validity(topology, 3, processes)


def test_complete_graph():
    """
    Test the CompleteGraph topology.
    """
    for size in [2, 4, 9]:
        # Create a complete graph topology with 4 processes
        topology = CompleteGraph.of_size(size)
        _check_any_topology(topology, size)
        _check_complete_graph_validity(topology, size)

    topology = CompleteGraph.from_([Pid(1), Pid(2), Pid(3)])
    _check_any_topology(topology, 3)
    _check_complete_graph_validity(topology, 3)
    
    processes = ProcessSet({Pid(10), Pid(20), Pid(30)})
    topology = CompleteGraph.from_(processes)
    _check_any_topology(topology, 3, processes)
    _check_complete_graph_validity(topology, 3, processes)
    

def test_star():
    """
    Test the Star topology.
    """
    for size in [2, 4, 9]:
        # Create a star topology with 4 processes
        topology = Star.of_size(size)
        _check_any_topology(topology, size)
        _check_star_validity(topology, size)
    
    process_list = [Pid(10), Pid(20), Pid(30), Pid(40)]
    processes = ProcessSet(process_list)
    topology = Star.from_(process_list[0], process_list[1:])
    _check_any_topology(topology, 4, processes)
    _check_star_validity(topology, 4, processes)

    with pytest.raises(ValueError):
        topology = Star.from_(process_list[0], process_list)
    with pytest.raises(ValueError):
        # Star topology must have at least 2 leaves
        topology = Star.from_(process_list[0], process_list[1:1])

def test_arbitrary():
    """
    Test the Arbitrary topology.
    """
    # Create an unconnected topology with 3 processes
    processes = ProcessSet({Pid(1), Pid(2), Pid(3)})
    topology = Arbitrary.from_(processes)
    _check_any_topology(topology, 3, processes)
    for pid in processes:
        assert topology.neighbors_of(pid) == ProcessSet()
        
    # Create a directed ring of 3 processes from tuples
    processes = ProcessSet({Pid(1), Pid(2), Pid(3)})
    channels = [
        (Pid(1), Pid(2)),
        (Pid(2), Pid(3)),
        (Pid(3), Pid(1)),
    ]
    topology = Arbitrary.from_(channels)
    _check_any_topology(topology, 3, processes)
    for pid in processes:
        assert len(topology.neighbors_of(pid)) == 1
        assert topology.neighbors_of(pid) == ProcessSet({Pid((pid.id % 3) + 1)})

    # Create an undirected ring of 3 processes from tuples
    processes = ProcessSet({Pid(1), Pid(2), Pid(3)})
    channels = [
        (Pid(1), Pid(2)),
        (Pid(2), Pid(3)),
        (Pid(3), Pid(1)),
    ]
    topology = Arbitrary.from_(channels, directed=False)
    _check_any_topology(topology, 3, processes)
    _check_ring_validity(topology, 3, processes)

    # Create an undirected ring of 3 processes from channels
    processes = ProcessSet({Pid(1), Pid(2), Pid(3)})
    channels = [
        Channel(Pid(1), Pid(2)),
        Channel(Pid(2), Pid(3)),
        Channel(Pid(3), Pid(1)),
    ]
    topology = Arbitrary.from_(channels, directed=False)
    _check_any_topology(topology, 3, processes)
    _check_ring_validity(topology, 3, processes)
    
    # Create an undirected ring of 3 processes from mixed objects
    processes = ProcessSet({Pid(1), Pid(2), Pid(3)})
    channels = [
        Pid(1),
        Pid(2),
        Channel(Pid(1), Pid(2)),
        (Pid(2), Pid(3)),
        Channel(Pid(3), Pid(1)),
    ]
    topology = Arbitrary.from_(channels, directed=False)
    _check_any_topology(topology, 3, processes)
    _check_ring_validity(topology, 3, processes)
    