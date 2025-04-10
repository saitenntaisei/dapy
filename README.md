# Dapy: Distributed Algorithms in Python

## Description

This is a simple (simplistic) programming framework to simulate the execution of distributed algorithms.



## How to begin (temporary)

The project is currently under active development with many changes to come in the near future.
Therefore, it is not yet recommended to install it as a fixed module.

### Requirements

The project was developed and tested using python version 3.13.2.
Although untested, it is likely to work with any version 3.11 and above.
The source code uses features that were introduced from python 3.11 and hence will not work with earlier versions of the interpreter.

### Setup: Initial steps

To use the environment, please follow the following steps:

1. clone this repository.
1. open a terminal in the root of the cloned project.
1. if you're using `pyenv` or `venv`, set then appropriately.
1. install the python package locally using the following `pip` command.
    ```shell
    pip install --editable .
    ```
    The flag `--editable` informs the `pip` command that the source code may change in the future and that changes should be taken into account. 
    This ensures that updates (and fixes) are taken into account whenever pulling commits, without requiring a further install.
    Although `pip` recommends to install this using `venv`, I personally install it on my regular python installation.
    This may be necessary if the name `dapy` conflicts with an existing package.
1. check if the install worked properly.
    Still from the root directory of the project, try to run the example as follows:
    ```shell
    python example.py
    ```
    The output should show some execution trace of the "Learn the Topology" algorithm in a ring of four processes.

### Getting Started

Look at the two parts annotated example that explains:
* [How to write an algorithm](docs/sample-algorithm.md)
* [How to define an execution](docs/sample-execution.md)

You can also check the following code template:
* [`examples/template.py`](examples/template.py)
