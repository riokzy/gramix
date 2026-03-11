import pytest
from gramix.router import Router
from gramix.filters import BaseFilter
from gramix.types.chat import Chat, ChatType
from gramix.types.user import User
from gramix.fsm import MemoryStorage, State, Step


class _Bot:
    pass


class _Msg:
    def __init__(self, text=None, from_id=1):
        self.text = text
        self.photo = None
        self.document = None
        self.video = None
        self.audio = None
        self.voice = None
        self.sticker = None
        self.forward_from = None
        self.reply_to_message = None
        self.poll = None
        self.location = None
        self.venue = None
        self.successful_payment = None
        self.chat = Chat(id=100, type=ChatType.PRIVATE)
        self.from_user = User(id=from_id, is_bot=False, first_name="A")
        self._bot = _Bot()


class _Cb:
    def __init__(self, data):
        self.data = data
        self.from_user = User(id=1, is_bot=False, first_name="A")
        self.message = None
        self.inline_message_id = None
        self.game_short_name = None
        self._bot = _Bot()


class Registration(State):
    name = Step()
    email = Step()


def test_router_message_handler_called():
    rt = Router()
    called = []

    @rt.message("/start")
    def h(msg):
        called.append(msg)

    assert rt.process_message(_Msg(text="/start"))
    assert len(called) == 1


def test_router_message_handler_not_called_wrong_command():
    rt = Router()
    called = []

    @rt.message("/start")
    def h(msg):
        called.append(msg)

    assert not rt.process_message(_Msg(text="/help"))
    assert called == []


def test_router_text_handler():
    rt = Router()
    called = []

    @rt.message("ping")
    def h(msg):
        called.append(True)

    assert rt.process_message(_Msg(text="ping"))
    assert called == [True]


def test_router_callback_handler():
    rt = Router()
    called = []

    @rt.callback("btn:ok")
    def h(cb):
        called.append(cb.data)

    assert rt.process_callback(_Cb("btn:ok"))
    assert called == ["btn:ok"]


def test_router_callback_prefix():
    rt = Router()
    called = []

    @rt.callback(prefix="item:")
    def h(cb):
        called.append(cb.data)

    assert rt.process_callback(_Cb("item:42"))
    assert not rt.process_callback(_Cb("menu:back"))
    assert called == ["item:42"]


def test_router_fsm_state_handler():
    storage = MemoryStorage()
    rt = Router(storage=storage)
    results = []

    @rt.state(Registration.name)
    def h(msg, state):
        results.append(state.current)

    ctx = storage.get(1)
    ctx.set(Registration.name)

    rt.process_message(_Msg(text="John", from_id=1))
    assert results == ["Registration.name"]


def test_router_fsm_takes_priority_over_message():
    storage = MemoryStorage()
    rt = Router(storage=storage)
    order = []

    @rt.message("/start")
    def msg_h(msg):
        order.append("message")

    @rt.state(Registration.name)
    def state_h(msg, state):
        order.append("state")

    storage.get(1).set(Registration.name)
    rt.process_message(_Msg(text="/start", from_id=1))
    assert order == ["state"]


def test_router_invalid_filter_type():
    rt = Router()
    with pytest.raises(TypeError):
        @rt.message(123)
        def h(msg):
            pass


def test_router_unknown_kwarg():
    rt = Router()
    with pytest.raises(TypeError):
        @rt.message(unknown="x")
        def h(msg):
            pass


def test_router_no_handler_returns_false():
    rt = Router()
    assert not rt.process_message(_Msg(text="/unknown"))


def test_router_poll_answer_handler():
    rt = Router()
    called = []

    @rt.poll_answer()
    def h(answer):
        called.append(answer)

    class _Answer:
        pass

    assert rt.process_poll_answer(_Answer())
    assert len(called) == 1


def test_router_successful_payment_handler():
    rt = Router()
    called = []

    @rt.successful_payment()
    def h(msg):
        called.append(msg)

    assert rt.process_successful_payment(_Msg())
    assert len(called) == 1
