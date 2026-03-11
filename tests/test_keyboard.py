import pytest
from gramix.types.keyboard import (
    BotCommand,
    ChatPermissions,
    Inline,
    InlineButton,
    RemoveKeyboard,
    Reply,
    ReplyButton,
)
from gramix.constants import MAX_CALLBACK_DATA_LENGTH


def test_inline_single_button():
    kb = Inline()
    kb.button("Click", callback="cb:1")
    d = kb.to_dict()
    assert len(d["inline_keyboard"]) == 1
    assert d["inline_keyboard"][0][0]["callback_data"] == "cb:1"


def test_inline_multiple_rows():
    kb = Inline()
    kb.button("A", callback="a")
    kb.row()
    kb.button("B", callback="b")
    d = kb.to_dict()
    assert len(d["inline_keyboard"]) == 2


def test_inline_url_button():
    kb = Inline()
    kb.button("Site", url="https://example.com")
    d = kb.to_dict()
    assert d["inline_keyboard"][0][0]["url"] == "https://example.com"


def test_inline_switch_inline():
    kb = Inline()
    kb.button("Search", switch_inline="query")
    d = kb.to_dict()
    assert d["inline_keyboard"][0][0]["switch_inline_query"] == "query"


def test_inline_callback_data_too_long():
    with pytest.raises(ValueError):
        btn = InlineButton(text="x", callback_data="a" * (MAX_CALLBACK_DATA_LENGTH + 1))
        btn.to_dict()


def test_inline_empty_row_not_added():
    kb = Inline()
    kb.row()
    d = kb.to_dict()
    assert d["inline_keyboard"] == []


def test_reply_keyboard_basic():
    kb = Reply()
    kb.button("Yes").button("No")
    d = kb.to_dict()
    assert len(d["keyboard"][0]) == 2
    assert d["resize_keyboard"] is True


def test_reply_keyboard_contact():
    kb = Reply()
    kb.button("Phone", contact=True)
    d = kb.to_dict()
    assert d["keyboard"][0][0].get("request_contact") is True


def test_reply_keyboard_placeholder():
    kb = Reply(placeholder="Type here")
    kb.button("Ok")
    d = kb.to_dict()
    assert d["input_field_placeholder"] == "Type here"


def test_remove_keyboard():
    d = RemoveKeyboard().to_dict()
    assert d == {"remove_keyboard": True}


def test_bot_command_strips_slash():
    cmd = BotCommand("/start", "Start bot")
    assert cmd.command == "start"
    d = cmd.to_dict()
    assert d["command"] == "start"
    assert d["description"] == "Start bot"


def test_bot_command_without_slash():
    cmd = BotCommand("help", "Help")
    assert cmd.command == "help"


def test_chat_permissions_to_dict():
    perms = ChatPermissions(can_send_messages=True, can_send_polls=True)
    d = perms.to_dict()
    assert d["can_send_messages"] is True
    assert d["can_send_polls"] is True
    assert d["can_invite_users"] is False


def test_chat_permissions_all_false_by_default():
    perms = ChatPermissions()
    d = perms.to_dict()
    assert all(v is False for v in d.values())
