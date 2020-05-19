# pyCEDLAR: Package to estimate Cumulative Effective dose and Lifetime attributable risk

``pyCEDLAR`` is a python package for estimating the cumulative effective dose (CED) and the lifetime attributable risk (LAR) after a fallout.

It is intended for nuclear regulatory bodies, for emergency preparedness and response. It is also intended for researchers and students in order to assess uncertainty propagation.

As a package, ``pyCEDLAR`` provides

- a set of constants (dose conversion factors etc)
- implementation of the formulae of C. Rääf et al.

The python package is rather intended for research, and a compiled version with a GUI intended for decision makers is available at [TODO](...).

Installation
------------

``pyCEDLAR`` can be installed by downloading the zipball from github.

```bash
   pip install https://github.com/ezsolti/pyCEDLAR/zipball/master
```

Installation was successfully tested on Linux and Windows.

Uninstall it with the command

```bash
   pip uninstall pyCEDLAR
```

Dependencies

- NumPy
- Scipy


Getting started
---------------

The theoretical background is summarized in C. Rääf et al. and the basic functionality is summarized at the [documentation site](https://ezsolti.github.io/pyCEDLAR/quickstart.html)

Examples
--------

Several examples can be found in the [examples folder](https://github.com/ezsolti/pyCEDLAR/tree/master/examples) or at the [documentation site](https://ezsolti.github.io/pyCEDLAR/examples.html)

Docs
----

API documentation, examples and theoretical background is covered at [ezsolti.github.io/pyCEDLAR](https://ezsolti.github.io/pyCEDLAR/)

Contributing, bugs, suggestions
-------------------------------

Any reported bug or suggestion is appreciated, please [open a new issue](https://github.com/ezsolti/pyCEDLAR/issues/new). If you would like to contribute, do not hesitate to do so, just include tests.

Tests
-----

Several tests can be found in the [tests folder](https://github.com/ezsolti/pyCEDLAR/tree/master/tests), run them with

```bash
python3 -m unittest discover tests/
```

Licence
-------

This work is licensed under the MIT License (see [LICENSE](https://github.com/ezsolti/pyCEDLAR/blob/master/LICENSE))

