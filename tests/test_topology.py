import pytest
from typing import Optional

from dapy.core.topology import *

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
    
    
    
def _check_ring(topology: Ring, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    
    indexed_processes = list(processes)
    
    # Check the neighbors of each process
    for i, pid in enumerate(processes):
        prev = indexed_processes[i-1]
        next = indexed_processes[(i+1)%size]
        assert len(topology.neighbors_of(pid)) == 2
        assert topology.neighbors_of(pid) == ProcessSet({prev, next})

def _check_complete_graph(topology: CompleteGraph, size: int, processes: Optional[ProcessSet] = None):
    if processes is None:
        processes = ProcessSet( Pid(i+1) for i in range(size))
    # Check the neighbors of each process
    for pid in processes:
        assert len(topology.neighbors_of(pid)) == size - 1
        assert topology.neighbors_of(pid) + {pid} == topology.processes()

def _check_star(topology: Star, size: int, processes: Optional[ProcessSet] = None):
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
        _check_ring(topology, size)
    
    processes = ProcessSet({Pid(10), Pid(20), Pid(30)})
    topology = Ring.from_(processes)
    _check_any_topology(topology, 3, processes)
    _check_ring(topology, 3, processes)


def test_complete_graph():
    """
    Test the CompleteGraph topology.
    """
    for size in [2, 4, 9]:
        # Create a complete graph topology with 4 processes
        topology = CompleteGraph.of_size(size)
        _check_any_topology(topology, size)
        _check_complete_graph(topology, size)

    topology = CompleteGraph.from_([Pid(1), Pid(2), Pid(3)])
    _check_any_topology(topology, 3)
    _check_complete_graph(topology, 3)
    
    processes = ProcessSet({Pid(10), Pid(20), Pid(30)})
    topology = CompleteGraph.from_(processes)
    _check_any_topology(topology, 3, processes)
    _check_complete_graph(topology, 3, processes)
    

def test_star():
    """
    Test the Star topology.
    """
    for size in [2, 4, 9]:
        # Create a star topology with 4 processes
        topology = Star.of_size(size)
        _check_any_topology(topology, size)
        _check_star(topology, size)
    
    process_list = [Pid(10), Pid(20), Pid(30), Pid(40)]
    processes = ProcessSet(process_list)
    topology = Star.from_(process_list[0], process_list[1:])
    _check_any_topology(topology, 4, processes)
    _check_star(topology, 4, processes)

