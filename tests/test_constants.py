from gramix.constants import (
    _SENTINEL,
    DEFAULT_TIMEOUT,
    MAX_MESSAGE_LENGTH,
    MAX_CAPTION_LENGTH,
    MAX_CALLBACK_DATA_LENGTH,
    ParseMode,
    POLLING_TIMEOUT,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
    RETRY_BACKOFF,
)


def test_sentinel_is_singleton():
    assert _SENTINEL is _SENTINEL


def test_sentinel_is_not_none():
    assert _SENTINEL is not None


def test_sentinel_is_not_false():
    assert _SENTINEL is not False


def test_parse_mode_values():
    assert ParseMode.HTML == "HTML"
    assert ParseMode.MARKDOWN == "MarkdownV2"
    assert ParseMode.MARKDOWN_LEGACY == "Markdown"


def test_limits_are_positive():
    assert MAX_MESSAGE_LENGTH > 0
    assert MAX_CAPTION_LENGTH > 0
    assert MAX_CALLBACK_DATA_LENGTH > 0


def test_limits_relative_sizes():
    assert MAX_MESSAGE_LENGTH > MAX_CAPTION_LENGTH
    assert MAX_CAPTION_LENGTH > MAX_CALLBACK_DATA_LENGTH


def test_timeout_values():
    assert DEFAULT_TIMEOUT > 0
    assert POLLING_TIMEOUT > 0


def test_retry_values():
    assert RETRY_ATTEMPTS >= 1
    assert RETRY_DELAY > 0
    assert RETRY_BACKOFF > 1
