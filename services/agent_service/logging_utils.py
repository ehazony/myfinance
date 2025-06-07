import logging
from colorlog import ColoredFormatter
from config import AGENT_LOG_LEVEL, LOG_FORMAT


class SafeColoredFormatter(ColoredFormatter):
    """Colored formatter that inserts default values for custom fields."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        record.session = getattr(record, "session", "-")
        record.agent = getattr(record, "agent", "-")
        return super().format(record)


def setup_logging() -> None:
    """Configure colored logging for the agent service."""
    level = getattr(logging, AGENT_LOG_LEVEL.upper(), logging.INFO)

    formatter = SafeColoredFormatter(
        fmt=f"%(log_color)s{LOG_FORMAT}%(reset)s",
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
