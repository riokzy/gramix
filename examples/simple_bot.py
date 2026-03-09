from gramix import Bot, Dispatcher, Router, ParseMode
from gramix.env import load_env

load_env()

bot = Bot()
rt  = Router()
dp  = Dispatcher(bot)


@rt.message("/start")
def on_start(msg):
    msg.reply(
        f"Привет, <b>{msg.from_user.first_name}</b>!\n"
        "Отправь мне любое сообщение.",
        parse_mode=ParseMode.HTML,
    )


@rt.message("/help")
def on_help(msg):
    msg.reply(
        "/start — начало\n"
        "/help  — помощь\n"
        "/info  — информация"
    )


@rt.message("/info")
def on_info(msg):
    msg.reply(
        f"Chat ID: <code>{msg.chat.id}</code>\n"
        f"User ID: <code>{msg.from_user.id}</code>\n"
        f"Username: @{msg.from_user.username or '—'}",
        parse_mode=ParseMode.HTML,
    )


@rt.message()
def on_echo(msg):
    if msg.text:
        msg.reply(f"Эхо: {msg.text}")


dp.include(rt)

if __name__ == "__main__":
    dp.run()
