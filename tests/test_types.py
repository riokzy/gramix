from gramix.types.user import User
from gramix.types.chat import Chat, ChatType
from gramix.types.location import Location, Venue
from gramix.types.poll import Poll, PollOption, PollAnswer
from gramix.types.payment import LabeledPrice, OrderInfo, PreCheckoutQuery, SuccessfulPayment
from gramix.types.game import GameHighScore
from gramix.types.chat_member import ChatMemberUpdated
from gramix.types.inline_query import (
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InlineQueryResultGif,
    InlineQueryResultAudio,
)


def test_user_full_name_with_last():
    u = User(id=1, is_bot=False, first_name="John", last_name="Doe")
    assert u.full_name == "John Doe"


def test_user_full_name_without_last():
    u = User(id=1, is_bot=False, first_name="John")
    assert u.full_name == "John"


def test_user_mention_with_username():
    u = User(id=1, is_bot=False, first_name="John", username="johndoe")
    assert u.mention == "@johndoe"


def test_user_mention_without_username():
    u = User(id=42, is_bot=False, first_name="John")
    assert "42" in u.mention


def test_user_from_dict():
    u = User.from_dict({"id": 1, "is_bot": False, "first_name": "A"})
    assert u.id == 1
    assert u.first_name == "A"


def test_chat_is_private():
    c = Chat(id=1, type=ChatType.PRIVATE)
    assert c.is_private
    assert not c.is_group
    assert not c.is_channel


def test_chat_is_group():
    c = Chat(id=1, type=ChatType.GROUP)
    assert c.is_group


def test_chat_is_supergroup():
    c = Chat(id=1, type=ChatType.SUPERGROUP)
    assert c.is_group


def test_chat_display_name_title():
    c = Chat(id=1, type=ChatType.GROUP, title="My Group")
    assert c.display_name == "My Group"


def test_chat_display_name_first_last():
    c = Chat(id=1, type=ChatType.PRIVATE, first_name="A", last_name="B")
    assert c.display_name == "A B"


def test_chat_display_name_fallback():
    c = Chat(id=99, type=ChatType.PRIVATE)
    assert c.display_name == "99"


def test_location_from_dict():
    loc = Location.from_dict({"longitude": 37.6, "latitude": 55.7})
    assert loc.longitude == 37.6
    assert loc.latitude == 55.7


def test_venue_from_dict():
    v = Venue.from_dict({
        "location": {"longitude": 37.6, "latitude": 55.7},
        "title": "Place",
        "address": "Street 1",
    })
    assert v.title == "Place"
    assert v.location.longitude == 37.6


def test_poll_option_from_dict():
    opt = PollOption.from_dict({"text": "Yes", "voter_count": 5})
    assert opt.text == "Yes"
    assert opt.voter_count == 5


def test_poll_from_dict():
    p = Poll.from_dict({
        "id": "abc",
        "question": "Q?",
        "options": [{"text": "A", "voter_count": 1}],
        "total_voter_count": 1,
    })
    assert p.question == "Q?"
    assert len(p.options) == 1


def test_poll_answer_retracted():
    a = PollAnswer.from_dict({"poll_id": "x", "option_ids": []})
    assert a.retracted


def test_poll_answer_not_retracted():
    a = PollAnswer.from_dict({"poll_id": "x", "option_ids": [0]})
    assert not a.retracted


def test_labeled_price_to_dict():
    lp = LabeledPrice(label="Item", amount=500)
    assert lp.to_dict() == {"label": "Item", "amount": 500}


def test_order_info_from_dict():
    oi = OrderInfo.from_dict({"name": "Ivan"})
    assert oi.name == "Ivan"
    assert oi.email is None


def test_successful_payment_amount_decimal():
    sp = SuccessfulPayment(
        currency="RUB",
        total_amount=10000,
        invoice_payload="p",
        telegram_payment_charge_id="t",
        provider_payment_charge_id="p",
    )
    assert sp.amount_decimal == 100.0


def test_game_high_score_from_dict():
    u = {"id": 1, "is_bot": False, "first_name": "A"}
    gs = GameHighScore.from_dict({"position": 1, "user": u, "score": 999})
    assert gs.score == 999
    assert gs.position == 1


def test_chat_member_updated_joined():
    data = {
        "chat": {"id": 1, "type": "group"},
        "from": {"id": 2, "is_bot": False, "first_name": "A"},
        "date": 0,
        "old_chat_member": {"status": "left", "user": {"id": 3, "is_bot": False, "first_name": "B"}},
        "new_chat_member": {"status": "member", "user": {"id": 3, "is_bot": False, "first_name": "B"}},
    }
    upd = ChatMemberUpdated.from_dict(data)
    assert upd.joined
    assert not upd.left


def test_chat_member_updated_left():
    data = {
        "chat": {"id": 1, "type": "group"},
        "from": {"id": 2, "is_bot": False, "first_name": "A"},
        "date": 0,
        "old_chat_member": {"status": "member", "user": {"id": 3, "is_bot": False, "first_name": "B"}},
        "new_chat_member": {"status": "left", "user": {"id": 3, "is_bot": False, "first_name": "B"}},
    }
    upd = ChatMemberUpdated.from_dict(data)
    assert upd.left
    assert not upd.joined


def test_chat_member_updated_missing_user_fallback():
    data = {
        "chat": {"id": 1, "type": "group"},
        "from": {"id": 2, "is_bot": False, "first_name": "A"},
        "date": 0,
        "old_chat_member": {"status": "left"},
        "new_chat_member": {"status": "member"},
    }
    upd = ChatMemberUpdated.from_dict(data)
    assert upd.user.id == 0


def test_inline_result_article_to_dict():
    r = InlineQueryResultArticle(id="1", title="T", message_text="M")
    d = r.to_dict()
    assert d["type"] == "article"
    assert d["input_message_content"]["message_text"] == "M"


def test_inline_result_photo_to_dict():
    r = InlineQueryResultPhoto(id="1", photo_url="http://x.com/p.jpg", thumb_url="http://x.com/t.jpg")
    d = r.to_dict()
    assert d["type"] == "photo"
    assert "photo_url" in d


def test_inline_result_gif_to_dict():
    r = InlineQueryResultGif(id="1", gif_url="http://x.com/g.gif", thumb_url="http://x.com/t.jpg")
    d = r.to_dict()
    assert d["type"] == "gif"


def test_inline_result_audio_to_dict():
    r = InlineQueryResultAudio(id="1", audio_url="http://x.com/a.mp3", title="Song")
    d = r.to_dict()
    assert d["type"] == "audio"
    assert d["title"] == "Song"
