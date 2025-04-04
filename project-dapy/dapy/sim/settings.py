from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Settings:
    """
    Class to represent the settings of a simulation.
    """
    is_verbose: bool = False
    is_debug: bool = False
    enable_trace: bool = False
