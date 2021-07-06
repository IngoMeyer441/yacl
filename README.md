# YACL - Yet Another Color Logger

## Overview

YACL is a very simple to use color logger for Python intended to be used for stderr logging. It can be set up with a
single function call in existing projects and enables colored logging output with reasonable defaults. Colors are
disabled automatically if stderr is not connected to a tty (e.g. on file redirection) or if not supported by the
connected terminal. Currently, Linux and macOS are supported.

You can use Markdown style formattings to produce bold and italic text. Additionally, text enclosed in double
underscores will be displayed underlined. YACL checks the terminal capabilities and automatically disables unsupported
formats.

## Installation

YACL is available on PyPI for Python 3.3+ and can be installed with `pip`:

```bash
python3 -m pip install yacl
```

If you use Arch Linux or one of its derivatives, you can also install `yacl` from the
[AUR](https://aur.archlinux.org/packages/python-yacl/):

```bash
yay -S python-yacl
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

![screenshot_simple](https://raw.githubusercontent.com/IngoMeyer441/yacl/master/simple.png)

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

  _attribute_colors = {
      "funcName": TerminalColorCodes.blue,
      "lineno": TerminalColorCodes.yellow,
      "name": TerminalColorCodes.cyan,
  }
  ```

- `keyword_colors`: A dictionary which assigns colors to a given regular expressions. This setting can be used to
  highlight expressions in the logging messages. This dictionary is merged with the internal defaults:

  ```python
  from yacl import TerminalColorCodes

  keyword_colors = {
      r"\bcritical( error)?\b": TerminalColorCodes.red + TerminalColorCodes.blink + TerminalColorCodes.bold,
      r"\bdebug(ged|ging)?\b": TerminalColorCodes.green + TerminalColorCodes.bold,
      r"\berror\b": TerminalColorCodes.red + TerminalColorCodes.bold,
      r"\bfail(ed|ing)?\b": TerminalColorCodes.red + TerminalColorCodes.bold,
      r"\binfo\b": TerminalColorCodes.blue + TerminalColorCodes.bold,
      r"\bwarn(ed|ing)?\b": TerminalColorCodes.yellow + TerminalColorCodes.bold,
      r'"[^"]*"': TerminalColorCodes.yellow,
      r"\*([^*]+)\*": TerminalColorCodes.italics,
      r"\*\*([^*]+)\*\*": TerminalColorCodes.bold,
      r"__([^_]+)__": TerminalColorCodes.underline,
      r"`([^`]+)`": TerminalColorCodes.standout,
  }
  ```

  Example: Pass a dictionary

  ```python
  {
      r"'[^']*'": TerminalColorCodes.green + TerminalColorCodes.italics,
  }
  ```

  to highlight strings in single quotes with green color and italic font (if supported by the Terminal).

- `level_colors`: A dictionary which assigns colors to logging levels (DEBUG, INFO, ...). This dictionary is merged with
  the internal defaults:

  ```python
  from yacl import TerminalColorCodes

  level_colors = {
      "DEBUG": TerminalColorCodes.green + TerminalColorCodes.bold,
      "INFO": TerminalColorCodes.blue + TerminalColorCodes.bold,
      "WARNING": TerminalColorCodes.yellow + TerminalColorCodes.bold,
      "ERROR": TerminalColorCodes.red + TerminalColorCodes.bold,
      "CRITICAL": TerminalColorCodes.red + TerminalColorCodes.blink + TerminalColorCodes.bold,
  }
  ```

### Colored Exceptions

If [Pygments](https://pypi.org/project/Pygments/) is installed, YACL exports an additonal function
`setup_colored_exceptions` to generate colored exception tracebacks. You can force to install Pygments as a YACL
dependency with the `colored_exceptions` extra:

```bash
python3 -m pip install 'yacl[colored_exceptions]'
```

The function `setup_colored_exceptions` needs to be called once (for example after `setup_colored_stderr_logging`) to
install a custom [Python excepthook](https://docs.python.org/3/library/sys.html#sys.excepthook). It takes an optional
bool parameter `dark_background` which can be set to `True` to activate brighter colors on dark terminal backgrounds. A
full example is:

```python
#!/usr/bin/env python3

import logging
from yacl import setup_colored_exceptions, setup_colored_stderr_logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    setup_colored_stderr_logging()
    setup_colored_exceptions()


if __name__ == "__main__":
    main()
```

## Contributing

Please open [an issue on GitHub](https://github.com/IngoMeyer441/yacl/issues/new) if you experience bugs or miss
features. Please consider to send a pull request if you can spend time on fixing the issue yourself. This project uses
[pre-commit](https://pre-commit.com) to ensure code quality and a consistent code style. Run

```bash
make git-hooks-install
```

to install all linters as Git hooks in your local clone of `yacl`.
