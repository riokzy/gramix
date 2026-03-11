from gramix import Bot, Dispatcher, Router, F, ParseMode, load_env

load_env()

bot = Bot(parse_mode=ParseMode.HTML)
dp  = Dispatcher(bot)
rt  = Router()
dp.include(rt)

@rt.message("/start")
def on_start(msg):
    msg.answer(
        "<b>gramix v0.1.7 — локации и места</b>\n\n"
        "/location — отправить точку на карте\n"
        "/venue — отправить место с названием\n"
        "/live — отправить живую геолокацию\n"
        "Отправь мне свою геолокацию — я её обработаю"
    )

@rt.message("/location")
def cmd_location(msg):
    bot.send_location(
        chat_id=msg.chat.id,
        latitude=55.7558,
        longitude=37.6173,
    )
    msg.answer("Вот Москва на карте!")

@rt.message("/venue")
def cmd_venue(msg):
    bot.send_venue(
        chat_id=msg.chat.id,
        latitude=55.7558,
        longitude=37.6173,
        title="Красная площадь",
        address="Красная площадь, Москва",
        foursquare_id="4adcda04f964a52077e71fe3",
    )

@rt.message("/live")
def cmd_live(msg):
    bot.send_location(
        chat_id=msg.chat.id,
        latitude=55.7558,
        longitude=37.6173,
        live_period=300,
    )
    msg.answer("Живая геолокация активна на 5 минут.")

@rt.message(F.location)
def on_location(msg):
    loc = msg.location
    parts = [f"Получена геолокация: <b>{loc.latitude}, {loc.longitude}</b>"]
    if loc.horizontal_accuracy:
        parts.append(f"Точность: {loc.horizontal_accuracy} м")
    if loc.heading:
        parts.append(f"Направление: {loc.heading}°")
    if loc.live_period:
        parts.append(f"Живая, период: {loc.live_period} с")
    msg.answer("\n".join(parts))

@rt.message(F.venue)
def on_venue(msg):
    v = msg.venue
    msg.answer(
        f"Получено место: <b>{v.title}</b>\n"
        f"Адрес: {v.address}\n"
        f"Координаты: {v.location.latitude}, {v.location.longitude}"
    )

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    dp.run()
