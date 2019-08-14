import logging
import os
import re
import subprocess
import sys
from typing import Dict, Match, Optional, Tuple

__author__ = "Ingo Heimbach"
__email__ = "i.heimbach@fz-juelich.de"
__copyright__ = "Copyright © 2019 Forschungszentrum Jülich GmbH. All rights reserved."
__license__ = "MIT"
__version_info__ = (0, 2, 0)
__version__ = ".".join(map(str, __version_info__))


DEFAULT_FORMAT_STRING = "[%(levelname)s] (%(name)s:%(lineno)s:%(funcName)s): %(message)s"


class _TerminalColorCodesMeta(type):
    class InitializingTerminalCodesFailedError(Exception):
        pass

    def __init__(cls, name: str, bases: Tuple[type], nmspc: Dict[str, str]) -> None:
        super().__init__(name, bases, nmspc)
        cls._initialized_terminal_codes = False
        cls._codes = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "purple": "\033[35m",
            "cyan": "\033[36m",
            "gray": "\033[37m",
            "light_black": "\033[90m",
            "light_red": "\033[91m",
            "light_green": "\033[92m",
            "light_yellow": "\033[93m",
            "light_blue": "\033[94m",
            "light_purple": "\033[95m",
            "light_cyan": "\033[96m",
            "white": "\033[97m",
            "blink": None,
            "bold": None,
            "italics": None,
            "underline": None,
            "standout": None,
            "reset": "\033[0m",
        }
        cls._codename_to_capname = {
            "blink": "blink",
            "bold": "bold",
            "italics": "sitm",
            "underline": "smul",
            "standout": "smso",
        }

    def _init_terminal_codes(cls) -> None:
        if cls._initialized_terminal_codes:
            return
        if not cls.is_stderr_tty():
            for key, value in dict(cls._codes).items():
                cls._codes[key] = ""
            return
        if not cls.has_terminal_color():
            for color_name in (
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
            ):
                cls._codes[color_name] = ""
        for key, value in dict(cls._codes).items():
            if value is None:
                try:
                    cls._codes[key] = cls._query_terminfo_database(key)
                except subprocess.CalledProcessError:
                    cls._codes[key] = ""
        cls._initialized_terminal_codes = True

    def _query_terminfo_database(cls, codename: str) -> str:
        if codename in cls._codename_to_capname:
            capname = cls._codename_to_capname[codename]
        else:
            capname = codename
        return str(subprocess.check_output(["tput", capname], universal_newlines=True))

    def is_stderr_tty(cls) -> bool:
        return os.isatty(sys.stderr.fileno())

    def has_terminal_color(cls) -> bool:
        try:
            return cls.is_stderr_tty() and int(cls._query_terminfo_database("colors")) >= 8
        except subprocess.CalledProcessError:
            return False

    @property
    def black(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["black"] is not None
        return cls._codes["black"]

    @property
    def red(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["red"] is not None
        return cls._codes["red"]

    @property
    def green(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["green"] is not None
        return cls._codes["green"]

    @property
    def yellow(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["yellow"] is not None
        return cls._codes["yellow"]

    @property
    def blue(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["blue"] is not None
        return cls._codes["blue"]

    @property
    def purple(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["purple"] is not None
        return cls._codes["purple"]

    @property
    def cyan(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["cyan"] is not None
        return cls._codes["cyan"]

    @property
    def gray(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["gray"] is not None
        return cls._codes["gray"]

    @property
    def light_black(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_black"] is not None
        return cls._codes["light_black"]

    @property
    def light_red(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_red"] is not None
        return cls._codes["light_red"]

    @property
    def light_green(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_green"] is not None
        return cls._codes["light_green"]

    @property
    def light_yellow(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_yellow"] is not None
        return cls._codes["light_yellow"]

    @property
    def light_blue(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_blue"] is not None
        return cls._codes["light_blue"]

    @property
    def light_purple(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_purple"] is not None
        return cls._codes["light_purple"]

    @property
    def light_cyan(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["light_cyan"] is not None
        return cls._codes["light_cyan"]

    @property
    def white(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["white"] is not None
        return cls._codes["white"]

    @property
    def blink(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["blink"] is not None
        return cls._codes["blink"]

    @property
    def bold(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["bold"] is not None
        return cls._codes["bold"]

    @property
    def italics(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["italics"] is not None
        return cls._codes["italics"]

    @property
    def underline(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["underline"] is not None
        return cls._codes["underline"]

    @property
    def standout(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["standout"] is not None
        return cls._codes["standout"]

    @property
    def reset(cls) -> str:
        cls._init_terminal_codes()
        assert cls._codes["reset"] is not None
        return cls._codes["reset"]


class TerminalColorCodes(metaclass=_TerminalColorCodesMeta):
    pass


class ColoredFormatter(logging.Formatter):
    _attribute_colors = {
        "funcName": TerminalColorCodes.blue,
        "lineno": TerminalColorCodes.yellow,
        "name": TerminalColorCodes.cyan,
    }
    _keyword_colors = {
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
        for attr in ("attribute_colors", "keyword_colors", "level_colors"):
            setattr(self, attr, dict(getattr(self, "_" + attr)))
            if locals()[attr] is not None:
                getattr(self, attr).update(locals()[attr])

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

        for attr, color in self.attribute_colors.items():
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
