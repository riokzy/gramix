import pytest
from gramix.exceptions import (
    FileError,
    FilterError,
    FSMError,
    GramixError,
    MessageError,
    MiddlewareError,
    NetworkError,
    RetryAfterError,
    TelegramAPIError,
    TokenError,
    WebhookError,
)


def test_all_inherit_from_gramix_error():
    for cls in (
        TokenError, TelegramAPIError, NetworkError, RetryAfterError,
        MessageError, FSMError, FilterError, MiddlewareError,
        WebhookError, FileError,
    ):
        assert issubclass(cls, GramixError)


def test_telegram_api_error_attributes():
    exc = TelegramAPIError(400, "Bad Request")
    assert exc.code == 400
    assert exc.description == "Bad Request"
    assert "400" in str(exc)
    assert "Bad Request" in str(exc)


def test_retry_after_error_attributes():
    exc = RetryAfterError(30)
    assert exc.retry_after == 30
    assert exc.code == 429
    assert isinstance(exc, TelegramAPIError)


def test_retry_after_is_catchable_as_telegram_error():
    with pytest.raises(TelegramAPIError):
        raise RetryAfterError(5)


def test_gramix_error_is_exception():
    assert issubclass(GramixError, Exception)


def test_network_error_message():
    exc = NetworkError("timeout")
    assert "timeout" in str(exc)


def test_token_error_is_raiseable():
    with pytest.raises(TokenError):
        raise TokenError("no token")


def test_fsm_error_is_raiseable():
    with pytest.raises(FSMError):
        raise FSMError("invalid state")


def test_webhook_error_is_raiseable():
    with pytest.raises(WebhookError):
        raise WebhookError("no url")


def test_file_error_is_raiseable():
    with pytest.raises(FileError):
        raise FileError("not found")
