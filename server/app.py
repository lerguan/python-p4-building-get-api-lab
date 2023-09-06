#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakery_query = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakery_query]

    response = make_response(jsonify(bakeries_list), 200)

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_serialized = bakery.to_dict()
    response = make_response(jsonify(bakery_serialized), 200)

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [price.to_dict() for price in baked_price]
    response = make_response(jsonify(baked_goods_by_price_serialized), 200)

    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    most_expensive_good = (
        BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    )
    most_expensive_good_serialized = most_expensive_good.to_dict()

    response = make_response(jsonify(most_expensive_good_serialized), 200)

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
