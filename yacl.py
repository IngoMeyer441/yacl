import logging
import os
import re
import subprocess
import sys
from typing import Dict, Match, Optional

__author__ = "Ingo Heimbach"
__email__ = "i.heimbach@fz-juelich.de"
__copyright__ = "Copyright © 2019 Forschungszentrum Jülich GmbH. All rights reserved."
__license__ = "MIT"
__version_info__ = (0, 1, 1)
__version__ = ".".join(map(str, __version_info__))


DEFAULT_FORMAT_STRING = "[%(levelname)s] (%(name)s:%(lineno)s:%(funcName)s): %(message)s"


class TerminalColorCodes:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[37m"
    LIGHT_BLACK = "\033[90m"
    BLINK = "\033[5m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    _attribute_colors = {
        "funcName": TerminalColorCodes.BLUE,
        "lineno": TerminalColorCodes.YELLOW,
        "name": TerminalColorCodes.CYAN,
    }
    _keyword_colors = {
        r"critical( error)?": TerminalColorCodes.RED + TerminalColorCodes.BLINK + TerminalColorCodes.BOLD,
        r"debug(ged|ging)?": TerminalColorCodes.GREEN + TerminalColorCodes.BOLD,
        r"error": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
        r"fail(ed|ing)?": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
        r"info": TerminalColorCodes.BLUE + TerminalColorCodes.BOLD,
        r"warn(ed|ing)?": TerminalColorCodes.YELLOW + TerminalColorCodes.BOLD,
        r'"[^"]*"': TerminalColorCodes.YELLOW,
    }
    _level_colors = {
        "DEBUG": TerminalColorCodes.GREEN + TerminalColorCodes.BOLD,
        "INFO": TerminalColorCodes.BLUE + TerminalColorCodes.BOLD,
        "WARNING": TerminalColorCodes.YELLOW + TerminalColorCodes.BOLD,
        "ERROR": TerminalColorCodes.RED + TerminalColorCodes.BOLD,
        "CRITICAL": TerminalColorCodes.RED + TerminalColorCodes.BLINK + TerminalColorCodes.BOLD,
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
            def get_color(keyword: str) -> str:
                for regex, color in self._keyword_colors.items():
                    if re.match(regex, keyword, re.IGNORECASE):
                        return color
                raise KeyError(keyword)

            keyword = match_obj.group(1)
            return "{}{}{}".format(get_color(keyword), keyword, TerminalColorCodes.RESET)

        for attr, color in self.attribute_colors.items():
            if attr in ("levelname", "msg"):
                continue
            setattr(record, attr, "{}{}{}".format(color, getattr(record, attr), TerminalColorCodes.RESET))
        if record.levelname in self._level_colors:
            record.levelname = "{}{}{}".format(
                self._level_colors[record.levelname], record.levelname, TerminalColorCodes.RESET
            )
        record.msg = re.sub(
            r"({})".format("|".join(self._keyword_colors)), colorize_keyword, record.msg, flags=re.IGNORECASE
        )
        return logging.Formatter.format(self, record)


def has_terminal_color() -> bool:
    try:
        return os.isatty(sys.stderr.fileno()) and int(subprocess.check_output(["tput", "colors"])) >= 8
    except subprocess.CalledProcessError:
        return False


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
    if has_terminal_color():
        formatter = ColoredFormatter(
            format_string, attribute_colors, keyword_colors, level_colors
        )  # type: logging.Formatter
    else:
        formatter = logging.Formatter(format_string)
    stream_handler.setFormatter(formatter)
    if remove_other_handlers:
        logger.handlers = []
    logger.addHandler(stream_handler)
