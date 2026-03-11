from gramix import Bot, Dispatcher, Inline, ParseMode, Reply, Router
from gramix.env import load_env

load_env()

bot = Bot()
rt  = Router()
dp  = Dispatcher(bot)

def main_menu() -> Inline:
    kb = Inline()
    kb.button("📋 Команды", callback="menu:commands")
    kb.button("ℹ️ О боте",  callback="menu:about")
    kb.row()
    kb.button("🌐 Сайт", url="https://github.com/riokzy/gramix")
    return kb

@rt.message("/start")
def on_start(msg):
    kb = Reply(resize=True)
    kb.button("📋 Меню")
    msg.reply("Привет! Выбери раздел:", keyboard=kb)

@rt.message("📋 Меню")
def on_menu(msg):
    msg.reply("Главное меню:", keyboard=main_menu())

@rt.callback("menu:commands")
def on_commands(call):
    call.answer()
    text = (
        "📋 <b>Команды</b>\n\n"
        "<code>/start</code> — начало\n"
        "<code>/help</code>  — помощь"
    )
    kb = Inline()
    kb.button("🔙 Назад", callback="menu:back")
    call.message.edit(text, keyboard=kb, parse_mode=ParseMode.HTML)

@rt.callback("menu:about")
def on_about(call):
    call.answer()
    text = "Бот на <b>gramix</b> 🚀"
    kb = Inline()
    kb.button("🔙 Назад", callback="menu:back")
    call.message.edit(text, keyboard=kb, parse_mode=ParseMode.HTML)

@rt.callback("menu:back")
def on_back(call):
    call.answer()
    call.message.edit("Главное меню:", keyboard=main_menu())

dp.include(rt)

if __name__ == "__main__":
    dp.run()
