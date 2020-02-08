from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import CarSpendType, Car, CarSpend
from flask import jsonify, g, request
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
    response=jsonify([])
    response.status_code = 201
    return response