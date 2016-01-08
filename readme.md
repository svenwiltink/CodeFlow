[![GitHub version](https://badge.fury.io/gh/SvenWiltink%2FCodeFlow.svg)](https://badge.fury.io/gh/SvenWiltink%2FCodeFlow)
[![PyPI version](https://badge.fury.io/py/CodeFlow.svg)](https://badge.fury.io/py/CodeFlow)
[![Build Status](https://travis-ci.org/SvenWiltink/CodeFlow.svg?branch=master)](https://travis-ci.org/SvenWiltink/CodeFlow) [![Coverage Status](https://coveralls.io/repos/SvenWiltink/CodeFlow/badge.svg?branch=master&service=github)](https://coveralls.io/github/SvenWiltink/CodeFlow?branch=master)
Welcome to PyFlow!
===================


PyFlow is a small module capable of making workflows easy. Workflows are defined in a json format that is easy to read and the code is put in state classes that can be defined elsewhere.

---

### How to install ###

For now the easiest way to install PyFlow is to clone the source and run pip install. PyFlow might be added to pypi at a later stage to make it a bit easer.

---

### Usage ###
I have provided an example in the example dir. It is quite straight forward and can be run by the following command:
```
sven@GLaDOS ~/downloads/PyFlow> python example
```

It will output ```gotta love this magic``` if it reaches the doMagic state and as well as the success value in the last state.
