import logging

from services.agent_service.logging_utils import SafeColoredFormatter, setup_logging


def test_safe_formatter_handles_missing_fields():
    formatter = SafeColoredFormatter("%(log_color)s%(message)s%(reset)s", log_colors={"INFO": "green"})
    record = logging.LogRecord("test", logging.INFO, __file__, 0, "hello", args=(), exc_info=None)
    formatted = formatter.format(record)
    assert "hello" in formatted


def test_setup_logging_no_errors():
    setup_logging()
    logger = logging.getLogger("test_logger")
    logger.info("hello")
