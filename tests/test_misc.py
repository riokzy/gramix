"""Tests for gramix.exceptions and gramix.env."""
import os
import tempfile

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
from gramix.env import load_env


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

def test_all_exceptions_inherit_gramix_error():
    for exc_class in (
        TokenError,
        TelegramAPIError,
        NetworkError,
        RetryAfterError,
        MessageError,
        FSMError,
        FilterError,
        MiddlewareError,
        WebhookError,
        FileError,
    ):
        assert issubclass(exc_class, GramixError)


def test_telegram_api_error_attributes():
    err = TelegramAPIError(400, "Bad Request: chat not found")
    assert err.code == 400
    assert "400" in str(err)
    assert "Bad Request" in str(err)


def test_retry_after_error_attributes():
    err = RetryAfterError(30)
    assert err.retry_after == 30
    assert err.code == 429
    assert isinstance(err, TelegramAPIError)


def test_exceptions_can_be_raised_and_caught():
    with pytest.raises(GramixError):
        raise TokenError("No token")

    with pytest.raises(TelegramAPIError):
        raise RetryAfterError(5)


# ---------------------------------------------------------------------------
# load_env
# ---------------------------------------------------------------------------

def test_load_env_sets_variable():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("TEST_GRAMIX_VAR=hello\n")
        path = f.name

    os.environ.pop("TEST_GRAMIX_VAR", None)
    load_env(path)
    assert os.environ.get("TEST_GRAMIX_VAR") == "hello"
    os.unlink(path)


def test_load_env_strips_quotes():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write('QUOTED_VAR="my_value"\n')
        path = f.name

    os.environ.pop("QUOTED_VAR", None)
    load_env(path)
    assert os.environ.get("QUOTED_VAR") == "my_value"
    os.unlink(path)


def test_load_env_ignores_comments():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("# This is a comment\nCOMMENT_TEST=value\n")
        path = f.name

    os.environ.pop("COMMENT_TEST", None)
    load_env(path)
    assert os.environ.get("COMMENT_TEST") == "value"
    os.unlink(path)


def test_load_env_does_not_override_existing():
    os.environ["EXISTING_VAR"] = "original"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("EXISTING_VAR=overwritten\n")
        path = f.name

    load_env(path)
    assert os.environ["EXISTING_VAR"] == "original"
    os.unlink(path)
    del os.environ["EXISTING_VAR"]


def test_load_env_missing_file_does_not_raise():
    load_env("/nonexistent/path/.env")  # Should not raise
