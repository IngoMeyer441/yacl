# YACL - Yet Another Color Logger

## Overview

YACL is a very simple to use color logger for Python intended to be used for stderr logging. It can be set up with a
single function call in existing projects and enables colored logging output with reasonable defaults. Colors are
disabled automatically if stderr is not connected to a tty (e.g. on file redirection). Currently, Linux and macOS are
supported.

## Installation

YACL is available on PyPI for Python 3.3+ and can be installed with `pip`:

```bash
python3 -m pip install yacl
```

## Usage

### Simple

Call ``setup_colored_stderr_logging`` after the root logger has been set up, for example:

```python
#!/usr/bin/env python3

import logging
from yacl import setup_colored_stderr_logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    setup_colored_stderr_logging()


if __name__ == "__main__":
    main()
```

Afterwards, get module level loggers and use them without any further configuration:

```python
import logging


logger = logging.getLogger(__name__)


def my_func():
    logger.debug('Failed to open file "abc"')
```

You will get an output like:

![screenshot_simple](https://raw.githubusercontent.com/IngoHeimbach/yacl/master/simple.png)

This example only works if you don't attach any output handlers to loggers other than the root logger as recommended in
the [Python logging documentation](https://docs.python.org/3/library/logging.html):

> If you attach a handler to a logger and one or more of its ancestors, it may emit the same record multiple times. In
> general, you should not need to attach a handler to more than one logger - if you just attach it to the appropriate
> logger which is highest in the logger hierarchy, then it will see all events logged by all descendant loggers,
> provided that their propagate setting is left set to True. A common scenario is to attach handlers only to the root
> logger, and to let propagation take care of the rest.

### Customization

You can pass several arguments to the `setup_colored_stderr_logging` function to customize the logging behavior:

- `logger`: The logger which will be configured to print colored logging output to stderr. By default, the root logger
  is used.

- `format_string`: The format string to use for logging messages. By default the logging format
  `[%(levelname)s] (%(name)s:%(lineno)s:%(funcName)s): %(message)s` is used.

  **Important**: All formats must be passed as **string types**. For example, in the default format, ``lineno`` is given
  as string (`(%lineno)s`) and not as number (`(%lineno)d`).

- `remove_other_handlers`: Bool flag to remove all other output handlers on the given logger. Is set to `true` by
  default to avoid duplicate logging messages.

- `attribute_colors`: A dictionary which assigns colors to logging attributes (which are used in the logging format
  string). This dictionary is merged with the internal defaults:

  ```python
  from yacl import TerminalColorCodes

  attribute_colors = {
      "funcName": TerminalColorCodes.BLUE,
      "lineno": TerminalColorCodes.YELLOW,
      "name": TerminalColorCodes.CYAN,
  }
  ```

- `keyword_colors`: A dictionary which assigns colors to a given regular expressions. This setting can be used to
  highlight expressions in the logging messages. This dictionary is merged with the internal defaults:

  ```python
  from yacl import TerminalColorCodes

  keyword_colors = {
      r"\bcritical( error)?\b": TerminalColorCodes.RED + TerminalColorCodes.BLINK + TerminalColorCodes.BOLD,
      r"\bdebug(ged|ging)?\b": TerminalColorCodes.GREEN + TerminalColorCodes.BOLD,
      r"\berror\b": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
      r"\bfail(ed|ing)?\b": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
      r"\binfo\b": TerminalColorCodes.BLUE + TerminalColorCodes.BOLD,
      r"\bwarn(ed|ing)?\b": TerminalColorCodes.YELLOW + TerminalColorCodes.BOLD,
      r'"[^"]*"': TerminalColorCodes.YELLOW,
  }
  ```

  Example: Pass a dictionary

  ```python
  {
      r"'[^']*'": TerminalColorCodes.GREEN,
  }
  ```

  to highlight strings in single quotes with green color.

- `level_colors`: A dictionary which assigns colors to logging levels (DEBUG, INFO, ...). This dictionary is merged with
  the internal defaults:

  ```python
  from yacl import TerminalColorCodes

  level_colors = {
      "DEBUG": TerminalColorCodes.GREEN + TerminalColorCodes.BOLD,
      "INFO": TerminalColorCodes.BLUE + TerminalColorCodes.BOLD,
      "WARNING": TerminalColorCodes.YELLOW + TerminalColorCodes.BOLD,
      "ERROR": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
      "CRITICAL": TerminalColorCodes.RED + TerminalColorCodes.BLINK + TerminalColorCodes.BOLD,
  }
  ```
