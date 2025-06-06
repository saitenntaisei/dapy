# Dapy: Distributed Algorithms in Python

<p style="font-style:italic">
IMPORTANT:
This project is in a very early stage of development; use at your own risks.
</p>

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
1. if you're using `pyenv` or `venv`, set them appropriately.
    You can find instructions about [setting up virtual environment with `venv`](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/). This is a little cumbersome but ensures no conflicts with an existing installation.
1. then, install the python package locally using the following `pip` command.
    ```shell
    pip install --editable .
    ```
    The flag `--editable` informs the `pip` command that the source code may change in the future and that changes should be taken into account. 
    This ensures that updates (and fixes) are taken into account whenever pulling commits, without requiring a further install. See the note below about [virtual environments](#venv).
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

### Optional dependencies

Some additional features are available optionally:

* `json` enables a dump/load of any `Trace` object into a JSON string.

To enable a feature, (re-)install `dapy` using the following command (e.g., for the `json` feature):
```shell
pip install --editable ".[json]"
```

### <a name="venv"></a> About virtual environments

The install warns that installing `dapy` directly may possibly result in dependencies conflicts, but the risk is actually very small in this case, since the package has no mandatory dependencies.

Although `pip` recommends to install this using `venv`, I personally install it on my regular python installation.  

Nevertheless, should you want to protect your environment, you can follow instructions about installing it into a virtual environment, either [using `venv` directly](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) or [using it via `uv`](https://docs.astral.sh/uv/pip/environments/)
