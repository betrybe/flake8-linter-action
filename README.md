# flake8-linter-action

This action run Flake8 over a project and comment on PR the errors found.

### Install dependencies

```sh
make install
# or
python3 -m pip install -r requirements.txt
```

### Run tests

```sh
make test
# or
python3 -m pytest
```

### Run flake8

```sh
make flake8
# or
python3 -m flake8 --append-config=setup.cfg
```

### Build docker image

```sh
make build
# or
docker build . -t 'pytest_evaluator_action'
```

## Evaluator Action

To call the evaluator action you must create `.github/workflows/main.yml` in the project repo with the release version.

Check the latest release [here](https://github.com/betrybe/flake8-linter-action/releases).

```yml
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  evaluator_job:
    name: Evaluator Job
    runs-on: ubuntu-18.04
    steps:
      - uses: actions/checkout@v2
      - name: Flake8 Linter Step
        uses: betrybe/flake8-linter-action@v*
        id: flake8_linter
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.number }}


```

## Inputs

### `token`

**Required**

The GitHub token to use for making API requests.

### `pr_number`

**Required**

Pull Request number that trigger build.

## Configure rules and analysis via `setup.cfg`

In order to configure the ESLint analysis for your project, you must create or modify the `setup.cfg` file at the root of your project.

Here follows an example for `setup.cfg`:

```
# .flake8
#
# DESCRIPTION
#     Configuration file for the python linter flake8.
#
#     This configuration is based on the generic
#     configuration published on GitHub.
#
# AUTHOR
#     krnd
#
# VERSION
#     1.0
#
# SEE ALSO
#     http://flake8.pycqa.org/en/latest/user/options.html
#     http://flake8.pycqa.org/en/latest/user/error-codes.html
#     https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes
#     https://gist.github.com/krnd
#


[flake8]

################### PROGRAM ################################

# Specify the number of subprocesses that Flake8 will use to run checks in parallel.
jobs = auto


################### OUTPUT #################################

########## VERBOSITY ##########

# Increase the verbosity of Flake8’s output.
verbose = 0
# Decrease the verbosity of Flake8’s output.
quiet = 0


########## FORMATTING ##########

# Select the formatter used to display errors to the user.
format = default

# Print the total number of errors.
count = True
# Print the source code generating the error/warning in question.
show-source = True
# Count the number of occurrences of each error/warning code and print a report.
statistics = True


########## TARGETS ##########

# Redirect all output to the specified file.
output-file = .flake8.log
# Also print output to stdout if output-file has been configured.
tee = True


################### FILE PATTERNS ##########################

# Provide a comma-separated list of glob patterns to exclude from checks.
exclude =
    # git folder
    .git,
    # python cache
    __pycache__,
# Provide a comma-separate list of glob patterns to include for checks.
filename =
    *.py


################### LINTING ################################

########## ENVIRONMENT ##########

# Provide a custom list of builtin functions, objects, names, etc.
builtins =


########## OPTIONS ##########

# Report all errors, even if it is on the same line as a `# NOQA` comment.
disable-noqa = False

# Set the maximum length that any line (with some exceptions) may be.
max-line-length = 100
# Set the maximum allowed McCabe complexity value for a block of code.
max-complexity = 10
# Toggle whether pycodestyle should enforce matching the indentation of the opening bracket’s line.
# incluences E131 and E133
hang-closing = True


########## RULES ##########

# ERROR CODES
#
# E/W  - PEP8 errors/warnings (pycodestyle)
# F    - linting errors (pyflakes)
# C    - McCabe complexity error (mccabe)
#
# W503 - line break before binary operator

# Specify a list of codes to ignore.
ignore =
    W503
# Specify the list of error codes you wish Flake8 to report.
select =
    E,
    W,
    F,
    C
# Enable off-by-default extensions.
enable-extensions =


########## DOCSTRING ##########

# Enable PyFlakes syntax checking of doctests in docstrings.
doctests = True

# Specify which files are checked by PyFlakes for doctest syntax.
include-in-doctest =
# Specify which files are not to be checked by PyFlakes for doctest syntax.
exclude-in-doctest =
```

This example was get from this [Gist](https://gist.github.com/krnd/1f3fb6c05af365977e486c47cb7b4a72#file-flake8).

## See more details and references

- [Flake8 documentation v3.8.3](https://buildmedia.readthedocs.org/media/pdf/flake8/latest/flake8.pdf)
- [How to Use Flake8](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html)
- [Learn more about Github Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-a-docker-container-action)
