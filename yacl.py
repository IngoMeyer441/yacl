import logging
import os
import re
import subprocess
import sys
from traceback import format_exception
from types import TracebackType
from typing import Dict, Match, Optional, Tuple, Type

try:
    from pygments import highlight
    from pygments.formatters import TerminalFormatter
    from pygments.lexers import get_lexer_by_name

    _pygments_available = True
except ImportError:
    _pygments_available = False

__author__ = "Ingo Meyer"
__email__ = "i.meyer@fz-juelich.de"
__copyright__ = "Copyright © 2021 Forschungszentrum Jülich GmbH. All rights reserved."
__license__ = "MIT"
__version_info__ = (0, 4, 3)
__version__ = ".".join(map(str, __version_info__))


DEFAULT_FORMAT_STRING = "[%(levelname)s] (%(name)s:%(lineno)s:%(funcName)s): %(message)s"


def is_env_variable_enabled(env_variable: str) -> bool:
    if env_variable not in os.environ:
        return False
    value = os.environ[env_variable].strip().lower()
    return value in ("on", "enabled", "activated", "yes") or (value.isdigit() and int(value) != 0)


def is_env_variable_disabled(env_variable: str) -> bool:
    if env_variable not in os.environ:
        return False
    value = os.environ[env_variable].strip().lower()
    return value in ("off", "disabled", "deactivated", "no") or (value.isdigit() and int(value) == 0)


def is_stderr_tty() -> bool:
    return not is_env_variable_disabled("CLICOLOR") and (
        is_env_variable_enabled("CLICOLOR_FORCE") or os.isatty(sys.stderr.fileno())
    )


class _TerminalColorCodesMeta(type):
    class InitializingTerminalCodesFailedError(Exception):
        pass

    def __init__(cls, name: str, bases: Tuple[type], nmspc: Dict[str, str]) -> None:
        super().__init__(name, bases, nmspc)
        cls._codename_to_capname = {
            "black": "setaf 0",
            "red": "setaf 1",
            "green": "setaf 2",
            "yellow": "setaf 3",
            "blue": "setaf 4",
            "purple": "setaf 5",
            "cyan": "setaf 6",
            "gray": "setaf 7",
            "light_black": "setaf 8",
            "light_red": "setaf 9",
            "light_green": "setaf 10",
            "light_yellow": "setaf 11",
            "light_blue": "setaf 12",
            "light_purple": "setaf 13",
            "light_cyan": "setaf 14",
            "white": "setaf 15",
            "blink": "blink",
            "bold": "bold",
            "italics": "sitm",
            "standout": "smso",
            "underline": "smul",
            "reset": "sgr0",
        }
        cls._color_names = (
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "purple",
            "cyan",
            "gray",
            "light_black",
            "light_red",
            "light_green",
            "light_yellow",
            "light_blue",
            "light_purple",
            "light_cyan",
            "white",
        )
        cls._codename_to_terminal_code = {}  # type: Dict[str, str]
        cls._initialized_terminal_codes = False

    def _init_terminal_codes(cls) -> None:
        if cls._initialized_terminal_codes:
            return
        if not is_stderr_tty():
            cls._codename_to_terminal_code = {key: "" for key in cls._codename_to_capname.keys()}
        else:
            has_terminal_color = cls.has_terminal_color()
            for codename in cls._codename_to_capname.keys():
                if codename in cls._color_names and not has_terminal_color:
                    cls._codename_to_terminal_code[codename] = ""
                else:
                    try:
                        cls._codename_to_terminal_code[codename] = cls._query_terminfo_database(codename)
                    except subprocess.CalledProcessError:
                        cls._codename_to_terminal_code[codename] = ""
        cls._initialized_terminal_codes = True

    def _query_terminfo_database(cls, codename: str) -> str:
        if codename in cls._codename_to_capname:
            capname = cls._codename_to_capname[codename]
        else:
            capname = codename
        return str(subprocess.check_output(["tput"] + capname.split(), universal_newlines=True))

    def has_terminal_color(cls) -> bool:
        try:
            return not is_env_variable_disabled("CLICOLOR") and (
                is_env_variable_enabled("CLICOLOR_FORCE")
                or (is_stderr_tty() and int(cls._query_terminfo_database("colors")) >= 8)
            )
        except subprocess.CalledProcessError:
            return False

    @property
    def black(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["black"] is not None
        return cls._codename_to_terminal_code["black"]

    @property
    def red(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["red"] is not None
        return cls._codename_to_terminal_code["red"]

    @property
    def green(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["green"] is not None
        return cls._codename_to_terminal_code["green"]

    @property
    def yellow(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["yellow"] is not None
        return cls._codename_to_terminal_code["yellow"]

    @property
    def blue(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["blue"] is not None
        return cls._codename_to_terminal_code["blue"]

    @property
    def purple(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["purple"] is not None
        return cls._codename_to_terminal_code["purple"]

    @property
    def cyan(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["cyan"] is not None
        return cls._codename_to_terminal_code["cyan"]

    @property
    def gray(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["gray"] is not None
        return cls._codename_to_terminal_code["gray"]

    @property
    def light_black(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_black"] is not None
        return cls._codename_to_terminal_code["light_black"]

    @property
    def light_red(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_red"] is not None
        return cls._codename_to_terminal_code["light_red"]

    @property
    def light_green(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_green"] is not None
        return cls._codename_to_terminal_code["light_green"]

    @property
    def light_yellow(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_yellow"] is not None
        return cls._codename_to_terminal_code["light_yellow"]

    @property
    def light_blue(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_blue"] is not None
        return cls._codename_to_terminal_code["light_blue"]

    @property
    def light_purple(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_purple"] is not None
        return cls._codename_to_terminal_code["light_purple"]

    @property
    def light_cyan(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["light_cyan"] is not None
        return cls._codename_to_terminal_code["light_cyan"]

    @property
    def white(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["white"] is not None
        return cls._codename_to_terminal_code["white"]

    @property
    def blink(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["blink"] is not None
        return cls._codename_to_terminal_code["blink"]

    @property
    def bold(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["bold"] is not None
        return cls._codename_to_terminal_code["bold"]

    @property
    def italics(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["italics"] is not None
        return cls._codename_to_terminal_code["italics"]

    @property
    def underline(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["underline"] is not None
        return cls._codename_to_terminal_code["underline"]

    @property
    def standout(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["standout"] is not None
        return cls._codename_to_terminal_code["standout"]

    @property
    def reset(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codename_to_terminal_code["reset"] is not None
        return cls._codename_to_terminal_code["reset"]


class TerminalColorCodes(metaclass=_TerminalColorCodesMeta):
    pass


class ColoredFormatter(logging.Formatter):
    _attribute_colors = {
        "funcName": TerminalColorCodes.blue,
        "lineno": TerminalColorCodes.yellow,
        "name": TerminalColorCodes.cyan,
    }
    _keyword_colors = {
        r"\bcritical(?: error)?\b": TerminalColorCodes.red + TerminalColorCodes.blink + TerminalColorCodes.bold,
        r"\bdebug(?:ged|ging)?\b": TerminalColorCodes.green + TerminalColorCodes.bold,
        r"\berror\b": TerminalColorCodes.red + TerminalColorCodes.bold,
        r"\bfail(?:ed|ing)?\b": TerminalColorCodes.red + TerminalColorCodes.bold,
        r"\binfo\b": TerminalColorCodes.blue + TerminalColorCodes.bold,
        r"\bwarn(?:ed|ing)?\b": TerminalColorCodes.yellow + TerminalColorCodes.bold,
        r'"[^"]*"': TerminalColorCodes.yellow,
        r"\*([^*]+)\*": TerminalColorCodes.italics,
        r"\*\*([^*]+)\*\*": TerminalColorCodes.bold,
        r"__([^_]+)__": TerminalColorCodes.underline,
        r"`([^`]+)`": TerminalColorCodes.standout,
    }
    _level_colors = {
        "DEBUG": TerminalColorCodes.green + TerminalColorCodes.bold,
        "INFO": TerminalColorCodes.blue + TerminalColorCodes.bold,
        "WARNING": TerminalColorCodes.yellow + TerminalColorCodes.bold,
        "ERROR": TerminalColorCodes.red + TerminalColorCodes.bold,
        "CRITICAL": TerminalColorCodes.red + TerminalColorCodes.blink + TerminalColorCodes.bold,
    }

    def __init__(
        self,
        message_format: str,
        attribute_colors: Optional[Dict[str, str]] = None,
        keyword_colors: Optional[Dict[str, str]] = None,
        level_colors: Optional[Dict[str, str]] = None,
    ):
        super().__init__(message_format)
        cls = type(self)
        for attr in ("attribute_colors", "keyword_colors", "level_colors"):
            setattr(self, "_" + attr, dict(getattr(cls, "_" + attr)))
            if locals()[attr] is not None:
                getattr(self, "_" + attr).update(locals()[attr])

    def format(self, record: logging.LogRecord) -> str:
        def colorize_keyword(match_obj: Match[str]) -> str:
            def get_color_and_stripped_keyword(keyword: str) -> Tuple[str, str]:
                for regex, color in self._keyword_colors.items():
                    match_obj = re.match(regex, keyword, re.IGNORECASE)
                    if match_obj is not None:
                        if color and len(match_obj.groups()) > 0:
                            return color, match_obj.group(1)
                        else:
                            return color, match_obj.group(0)
                raise KeyError(keyword)

            keyword = match_obj.group(1)
            color, stripped_keyword = get_color_and_stripped_keyword(keyword)
            return "{}{}{}".format(color, stripped_keyword, TerminalColorCodes.reset)

        for attr, color in self._attribute_colors.items():
            if attr in ("levelname", "msg"):
                continue
            setattr(record, attr, "{}{}{}".format(color, getattr(record, attr), TerminalColorCodes.reset))
        if record.levelname in self._level_colors:
            record.levelname = "{}{}{}".format(
                self._level_colors[record.levelname], record.levelname, TerminalColorCodes.reset
            )
        record.msg = re.sub(
            r"({})".format("|".join(self._keyword_colors)), colorize_keyword, record.msg, flags=re.IGNORECASE
        )
        return logging.Formatter.format(self, record)


def setup_colored_stderr_logging(
    logger: Optional[logging.Logger] = None,
    format_string: str = DEFAULT_FORMAT_STRING,
    remove_other_handlers: bool = True,
    attribute_colors: Optional[Dict[str, str]] = None,
    keyword_colors: Optional[Dict[str, str]] = None,
    level_colors: Optional[Dict[str, str]] = None,
) -> None:
    if logger is None:
        logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    formatter = ColoredFormatter(format_string, attribute_colors, keyword_colors, level_colors)
    stream_handler.setFormatter(formatter)
    if remove_other_handlers:
        logger.handlers = []
    logger.addHandler(stream_handler)


if _pygments_available:

    def setup_colored_exceptions(dark_background: bool = False) -> None:
        def excepthook(typ: Type[BaseException], value: BaseException, traceback: TracebackType) -> None:
            traceback_text = "".join(format_exception(typ, value, traceback))
            lexer = get_lexer_by_name("pytb", stripall=True)
            formatter = TerminalFormatter(bg="dark" if dark_background else "light")
            sys.stderr.write(highlight(traceback_text, lexer, formatter))
            sys.stderr.flush()

        if TerminalColorCodes.has_terminal_color():
            sys.excepthook = excepthook
