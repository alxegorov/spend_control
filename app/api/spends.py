from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import CarSpendType, Car, CarSpend
from flask import jsonify, g, request
from sqlalchemy import desc
from dateutil import parser

@bp.route('/spends/move/car/cars', methods=['GET'])
@token_auth.login_required
def get_cars():
    data = []
    cars = Car.query.filter(Car.user_id == g.current_user.id)
    for car in cars:
        data.append({'id': car.id, 'value': car.model.manufacturer + ' ' + car.model.model})
    return jsonify(data)

@bp.route('/spends/move/car/types', methods=['GET'])
@token_auth.login_required
def get_car_spend_typs():
    return CarSpendType.to_json()

@bp.route('spends/move/car/newspend', methods=['POST'])
@token_auth.login_required
def new_spend():
    data = request.get_json()
    spend = CarSpend(timestamp=parser.parse(data['date']), trip=int(data['trip']), price=float(data['price']),
                     amount=float(data['mount']), car_id=int(data['car']), car_spend_type_id=int(data['type']))
    db.session.add(spend)
    db.session.commit()
    return 'OK'

@bp.route('spends/move/car/<int:id>/fuelconsumtion', methods=['GET'])
@token_auth.login_required
def get_fuel_consumption(id):
    fuel_types = []
    types = CarSpendType.query.filter(CarSpendType.type.like('Бензин%')).all()
    for t in types:
        fuel_types.append(t.id)
    fuel_spends = CarSpend.query.filter(CarSpend.car_id==id, CarSpend.car_spend_type_id.in_(fuel_types)).all()
    amount = 0
    for i in range(len(fuel_spends) - 1):
        amount = amount + fuel_spends[i].amount
    first_spend = fuel_spends[0]
    last_spend = fuel_spends[len(fuel_spends) - 1]
    trip = last_spend.trip - first_spend.trip
    if trip != 0:
        fuel_cons = {'fuel_consumtion': amount / trip * 100}
    else:
        fuel_cons = {'fuel_consumtion': 0}
    return jsonify(fuel_cons)
    

@bp.route('spends/move/car/<int:id>/kmprice', methods=['GET'])
@token_auth.login_required
def get_km_price(id):
    pass

@bp.route('spends/move/car/<int:id>/mounthprice', methods=['GET'])
@token_auth.login_required
def get_mounth_price(id):
    pass

@bp.route('spends/move/car/<int:id>/yearprice', methods=['GET'])
@token_auth.login_required
def get_year_price(id):
    pass