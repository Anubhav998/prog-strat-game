# Code Quality

This codebase holds itself to some of the highest standards in code quality and testing.

## Coverage

This codebase follows the pragma of 100% test coverage. The build will fail if 100% is not achieved.

Coverage is run during `fab test`, which is also executed during `fab cut`.

If your results do not come back with 100%, you can see what lines are missing with:

```
coverage report -m
```

Coverage is also externally reported with coveralls.

[![Coverage Status](https://coveralls.io/repos/mc706/prog-strat-game/badge.svg?branch=HEAD)](https://coveralls.io/r/mc706/prog-strat-game?branch=HEAD)


## Code Quality

This codebase follows a few code quality libraries, including pep8, pylint, flake8. It uses a tool called
[prospector](https://github.com/landscapeio/prospector) distributed by [landscape.io](https://landscape.io).

The build is contingent on `pep8` and `jshint`. However we report externally on [landscape.io](https://landscape.io).

[![Code Health](https://landscape.io/github/mc706/prog-strat-game/master/landscape.svg?style=flat)](https://landscape.io/github/mc706/prog-strat-game/master)

This project also uses [codacy](https://codacy.com)

[![Codacy Badge](https://www.codacy.com/project/badge/f6046e45c8cc436b86273f3edf9d5bef)](https://www.codacy.com/app/mcdevitt-ryan/prog-strat-game)


## Code Complexity

This codebase also uses code complexity tools to ensure maintainability. It uses [radon]() and CI cli tool [xenon]() to 
measure this.

To check the repo locally, you can run:

```
radon cc . -a
```

The following gets run as part of `fab quality_check`:

```
xenon . -a A -b A -m A -i core
```
