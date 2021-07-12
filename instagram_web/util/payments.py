from app import app
from config import Config
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id = app.config["MERCHANT_ID"],
        public_key = app.config["PUBLIC_KEY"],
        private_key = app.config["PRIVATE_KEY"]
    )
)
