from app import app
from config import Config
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from instagram_web.util.payments import *
from models.donation import Donation
from models.image import Image
from decimal import Decimal
import requests

donations_blueprint = Blueprint('donations', __name__, template_folder='templates')

# create a new donation
@donations_blueprint.route("/", methods=["POST"])
@login_required
def create():
    nonce = request.form['nonce']
    amount_input = Decimal(request.form['amount'])
    amount = round(amount_input)
    image = request.form['image_id']
    sender = current_user
    if nonce and amount:
        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success and result.transaction:
            donation = Donation(amount=amount, image=image, sender=sender.id)
            if donation.save():
                image = Image.get_or_none(Image.id == image)
                if image:
                    user = image.user
                    notify_creator = requests.post(
                    		"https://api.mailgun.net/v3/sandbox638887e0639f44538b33f3c0a8a7b0f6.mailgun.org/messages",
                    		auth=("api", app.config["MAILGUN_API_KEY"]),
                    		data={"from": "de:fine <mailgun@sandbox638887e0639f44538b33f3c0a8a7b0f6.mailgun.org>",
                    			"to": [user.email],
                    			"subject": "Hello",
                    			"text": "New donation!"})
                    notify_sender = requests.post(
                    		"https://api.mailgun.net/v3/sandbox638887e0639f44538b33f3c0a8a7b0f6.mailgun.org/messages",
                    		auth=("api", app.config["MAILGUN_API_KEY"]),
                    		data={"from": "de:fine <mailgun@sandbox638887e0639f44538b33f3c0a8a7b0f6.mailgun.org>",
                    			"to": [sender.email],
                    			"subject": "Thank You!",
                    			"text": "Thank you for your kind donation!"})
                    flash("Thank you for your kind donation!")
                    return redirect(url_for('users.show', username=user.username, image=image))
    flash("Oh no, an error occurred", "error")
    return render_template('posts/show.html', id=id)
