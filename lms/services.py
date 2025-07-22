import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(payment):
    price = stripe.Price.create(
        currency="RUB",
        unit_amount=payment.payment_amount * 100,
        product_data={"name": payment.course.title, "id": payment.course.id},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 2}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
