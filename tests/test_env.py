import os
import tempfile
import pytest
from gramix.env import load_env, get_token, is_debug, get_webhook_url
from gramix.constants import TOKEN_ENV_KEY, DEBUG_ENV_KEY, WEBHOOK_URL_ENV_KEY


def _write_env(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return f.name


def _clear(*keys):
    for k in keys:
        os.environ.pop(k, None)


def test_load_env_sets_variable():
    path = _write_env("TEST_GRAMIX_VAR=hello\n")
    _clear("TEST_GRAMIX_VAR")
    load_env(path)
    assert os.environ.get("TEST_GRAMIX_VAR") == "hello"
    _clear("TEST_GRAMIX_VAR")
    os.unlink(path)


def test_load_env_strips_quotes():
    path = _write_env('QUOTED_VAR="my_value"\n')
    _clear("QUOTED_VAR")
    load_env(path)
    assert os.environ.get("QUOTED_VAR") == "my_value"
    _clear("QUOTED_VAR")
    os.unlink(path)


def test_load_env_does_not_override_existing():
    os.environ["EXISTING_VAR"] = "original"
    path = _write_env("EXISTING_VAR=new\n")
    load_env(path)
    assert os.environ["EXISTING_VAR"] == "original"
    _clear("EXISTING_VAR")
    os.unlink(path)


def test_load_env_skips_comments():
    path = _write_env("# this is a comment\nSOME_VAR=yes\n")
    _clear("SOME_VAR")
    load_env(path)
    assert os.environ.get("SOME_VAR") == "yes"
    _clear("SOME_VAR")
    os.unlink(path)


def test_load_env_missing_file_does_not_raise():
    load_env("/nonexistent/path/.env")


def test_get_token_returns_value():
    os.environ[TOKEN_ENV_KEY] = "tok123"
    assert get_token() == "tok123"
    _clear(TOKEN_ENV_KEY)


def test_get_token_returns_none_when_absent():
    _clear(TOKEN_ENV_KEY)
    assert get_token() is None


def test_is_debug_true():
    for val in ("1", "true", "yes", "TRUE", "YES"):
        os.environ[DEBUG_ENV_KEY] = val
        assert is_debug()
    _clear(DEBUG_ENV_KEY)


def test_is_debug_false():
    _clear(DEBUG_ENV_KEY)
    assert not is_debug()
    os.environ[DEBUG_ENV_KEY] = "0"
    assert not is_debug()
    _clear(DEBUG_ENV_KEY)


def test_get_webhook_url():
    os.environ[WEBHOOK_URL_ENV_KEY] = "https://example.com/hook"
    assert get_webhook_url() == "https://example.com/hook"
    _clear(WEBHOOK_URL_ENV_KEY)


def test_get_webhook_url_none():
    _clear(WEBHOOK_URL_ENV_KEY)
    assert get_webhook_url() is None
