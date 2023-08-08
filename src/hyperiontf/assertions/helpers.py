from typing import Any, Optional
from hyperiontf.logging.logger import Logger
from hyperiontf.typing import LoggerSource

from .expect import Expect


def _process_type(
    actual_value: Any,
    _value_type: Optional[str] = None,
    _content_type: Optional[str] = None,
) -> Any:
    return actual_value


def expect(
    actual_value: Any,
    value_type: Optional[str] = None,
    content_type: Optional[str] = None,
    logger: Optional[Logger] = None,
    sender: str = LoggerSource.EXPECT,
) -> Expect:
    return Expect(
        _process_type(actual_value, value_type, content_type),
        logger=logger,
        sender=sender,
        is_assertion=True,
    )


def verify(
    actual_value: Any,
    value_type: Optional[str] = None,
    content_type: Optional[str] = None,
    logger: Optional[Logger] = None,
    sender: str = LoggerSource.EXPECT,
) -> Expect:
    return Expect(
        _process_type(actual_value, value_type, content_type),
        logger=logger,
        sender=sender,
        is_assertion=False,
    )
