import pytest

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


def test_ring():
    """
    Test the Ring topology.
    """
    for size in [2, 4, 9]:
        size = 4
        # Create a ring topology with 4 processes
        topology = Ring.of_size(size)
        processes = ProcessSet( Pid(i+1) for i in range(size))
        
        assert topology.processes() == processes
        assert len(topology) == size
        assert len(topology.processes()) == size
        assert Pid(0) not in topology
        assert Pid(1) in topology
        assert Pid(size) in topology
        assert Pid(size+1) not in topology
        
        _all_processes_are_present(topology, processes)
        _no_process_is_its_own_neighbor(topology)
        
        # Check the neighbors of each process
        for pid in processes:
            prev = Pid(size) if pid == Pid(1) else Pid(pid.id - 1)
            next = Pid(1) if pid == Pid(size) else Pid(pid.id + 1)
            assert len(topology.neighbors_of(pid)) == 2
            assert topology.neighbors_of(pid) == ProcessSet({prev, next})


def test_complete_graph():
    """
    Test the CompleteGraph topology.
    """
    for size in [2, 4, 9]:
        # Create a complete graph topology with 4 processes
        topology = CompleteGraph.of_size(size)
        processes = ProcessSet( Pid(i+1) for i in range(size))
        
        assert topology.processes() == processes
        assert len(topology) == size
        assert len(topology.processes()) == size
        assert Pid(0) not in topology
        assert Pid(1) in topology
        assert Pid(size) in topology
        assert Pid(size+1) not in topology

        _all_processes_are_present(topology, processes)
        _no_process_is_its_own_neighbor(topology)
        
        # Check the neighbors of each process
        for pid in processes:
            assert len(topology.neighbors_of(pid)) == size - 1
            assert topology.neighbors_of(pid) + {pid} == topology.processes()

        
def test_star():
    """
    Test the Star topology.
    """
    for size in [2, 4, 9]:
        # Create a star topology with 4 processes
        topology = Star.of_size(size)
        processes = ProcessSet( Pid(i+1) for i in range(size))
        
        assert topology.processes() == processes
        assert len(topology) == size
        assert len(topology.processes()) == size
        assert Pid(0) not in topology
        assert Pid(1) in topology
        assert Pid(size) in topology
        assert Pid(size+1) not in topology

        _all_processes_are_present(topology, processes)
        _no_process_is_its_own_neighbor(topology)
        
        # Check the neighbors of each process
        for pid in processes:
            if pid == Pid(1):
                assert len(topology.neighbors_of(pid)) == size - 1
                assert topology.neighbors_of(pid) + {pid} == topology.processes()
            else:
                assert len(topology.neighbors_of(pid)) == 1
                assert topology.neighbors_of(pid) == ProcessSet({Pid(1)})
