from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from instagram_web.util.payments import *
from models.donation import Donation
from decimal import Decimal

donations_blueprint = Blueprint('donations', __name__, template_folder='templates')

# create a new donation
@donations_blueprint.route("/", methods=["POST"])
@login_required
def create():
    nonce = request.form['nonce']
    amount_input = Decimal(request.form['amount'])
    amount = round(amount_input)
    id = request.form['image_id']
    if nonce and amount:
        gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        donation = Donation(amount=amount, image=id)
        if donation.save():
            flash("Thank you for your kind donation!")
            return redirect(url_for('users.index'))
        else:
            flash("Oh no, an error occurred", "error")
            return render_template('posts/show.html', id=id)
    else:
        flash("Oh no, an error occurred", "error")
        return render_template('posts/show.html', id=id)
