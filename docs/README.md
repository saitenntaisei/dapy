---
layout: page
title: Index page for project dapy
permalink: /dapy/
---

# Documentation

This project is still in its infancy; hence the documentation is still very scarce, but you may possibly find the following to be useful:

* [`API doc`](api/) generated automatically from the docstrings.
* sample code:
    * [`sample-algorithm.md`]({% link sample-algorithm.md %}) illustrates how to define an algorithm
    * [`sample-execution.md`]({% link sample-execution.md %}) illustrates how to run a distributed execution


## Generate API Documentation

Install pdoc if necessary:
```shell
pip install pdoc
```

Generate the docs:
```shell
pdoc -o docs/api -d google src/dapy
```

Open the docs (using open command on Mac terminal):
```shell
open docs/api/index.html
```
