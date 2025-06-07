import logging
from colorlog import ColoredFormatter
from config import AGENT_LOG_LEVEL


def setup_logging() -> None:
    """Configure colored logging for the agent service."""
    level = getattr(logging, AGENT_LOG_LEVEL.upper(), logging.INFO)

    formatter = ColoredFormatter(
        fmt="%(log_color)s%(asctime)s [%(levelname)s] %(session)s %(agent)s %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
