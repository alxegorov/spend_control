from app.api import bp
from app.api.auth import token_auth
from app.models import CarSpendType, Car
from flask import jsonify, g

@bp.route('/spends/move/cars', methods=['GET'])
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