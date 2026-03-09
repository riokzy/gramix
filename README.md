# gramix

[![PyPI](https://img.shields.io/pypi/v/gramix)](https://pypi.org/project/gramix)
[![Python](https://img.shields.io/pypi/pyversions/gramix)](https://pypi.org/project/gramix)
[![License](https://img.shields.io/pypi/l/gramix)](LICENSE)

Мощный фреймворк для создания Telegram ботов на Python.

```
pip install gramix
```

---

## Примеры

**Простой бот**

```python
from gramix import Bot, Dispatcher, Router
from gramix.env import load_env

load_env()

bot = Bot()
rt  = Router()
dp  = Dispatcher(bot)

@rt.message("/start")
def on_start(msg):
    msg.reply(f"Привет, {msg.from_user.first_name}!")

@rt.message()
def echo(msg):
    msg.reply(msg.text)

dp.include(rt)
dp.run()
```

**Inline клавиатура**

```python
from gramix import Inline

@rt.message("/menu")
def on_menu(msg):
    kb = Inline()
    kb.button("Да", callback="yes")
    kb.button("Нет", callback="no")
    msg.reply("Выбери:", keyboard=kb)

@rt.callback("yes")
def on_yes(call):
    call.answer("Отлично!")
    call.message.edit("✅ Выбрано: Да")
```

**FSM**

```python
from gramix import State, Step

class Form(State):
    name = Step()
    age  = Step()

@rt.message("/start")
def on_start(msg):
    state = rt.fsm.get(msg.from_user.id)
    state.set(Form.name)
    msg.reply("Как тебя зовут?")

@rt.state(Form.name)
def get_name(msg, state):
    state.data["name"] = msg.text
    state.next()
    msg.reply("Сколько лет?")

@rt.state(Form.age)
def get_age(msg, state):
    name = state.data["name"]
    state.finish()
    msg.reply(f"{name}, {msg.text} лет — записал.")
```

**Async**

```python
@rt.message("/start")
async def on_start(msg):
    await msg.answer("Привет!")

dp.run_async()
```

Больше примеров в папке [`examples/`](examples/).

---

## Лицензия

MIT © riokzy
