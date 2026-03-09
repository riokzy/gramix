from gramix import (
    Bot, Dispatcher, Router,
    PreCheckoutQuery, SuccessfulPayment, LabeledPrice,
    ParseMode, load_env,
)

load_env()

bot = Bot(parse_mode=ParseMode.HTML)
dp  = Dispatcher(bot)
rt  = Router()
dp.include(rt)

PROVIDER_TOKEN = "YOUR_PROVIDER_TOKEN"


@rt.message("/start")
def on_start(msg):
    msg.answer(
        "<b>gramix v0.1.7 — платежи</b>\n\n"
        "/buy — купить товар (100 RUB)\n"
        "/donate — задонатить произвольную сумму"
    )


@rt.message("/buy")
def cmd_buy(msg):
    bot.send_invoice(
        chat_id=msg.chat.id,
        title="Тестовый товар",
        description="Это тестовая покупка через gramix.",
        payload="test_item_001",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Тестовый товар", amount=10000)],
        photo_url="https://via.placeholder.com/256",
        photo_width=256,
        photo_height=256,
    )


@rt.message("/donate")
def cmd_donate(msg):
    bot.send_invoice(
        chat_id=msg.chat.id,
        title="Донат",
        description="Поддержи разработку gramix.",
        payload="donation",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label="Донат", amount=5000)],
        max_tip_amount=50000,
        suggested_tip_amounts=[5000, 10000, 25000, 50000],
    )


@rt.pre_checkout_query()
def on_pre_checkout(query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(query.id, ok=True)


@rt.successful_payment()
def on_payment(msg):
    payment: SuccessfulPayment = msg.successful_payment
    msg.answer(
        f"Спасибо за оплату! ✅\n"
        f"Сумма: <b>{payment.amount_decimal} {payment.currency}</b>\n"
        f"Payload: <code>{payment.invoice_payload}</code>"
    )


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    dp.run()
