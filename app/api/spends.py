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
    return jsonify(CarSpendType.to_json())

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
        amount += fuel_spends[i].amount
    first_spend = fuel_spends[0]
    last_spend = fuel_spends[len(fuel_spends) - 1]
    trip = last_spend.trip - first_spend.trip
    if trip != 0:
        fuel_cons = {'fuel_consumtion': round((amount / trip * 100), 1)}
    else:
        fuel_cons = {'fuel_consumtion': 0}
    return jsonify(fuel_cons)
    

@bp.route('spends/move/car/<int:id>/kmprice', methods=['GET'])
@token_auth.login_required
def get_km_price(id):
    spends = CarSpend.query.filter(CarSpend.car_id==id).all()
    price = 0
    for s in spends:
        price += s.price * s.amount
    first_spend = spends[0]
    last_spend = spends[len(spends) - 1]
    trip = last_spend.trip - first_spend.trip
    if trip != 0:
        unit_price = {'unit_price': round((price / trip), 2)}
    else:
        unit_price = {'unit_price': 0}
    return jsonify(unit_price)

@bp.route('spends/move/car/<int:id>/mounthprice', methods=['GET'])
@token_auth.login_required
def get_mounth_price(id):
    spends = CarSpend.query.filter(CarSpend.car_id==id).all()
    price = 0
    for s in spends:
        price += s.price * s.amount
    first_spend = spends[0]
    last_spend = spends[len(spends) - 1]
    days = last_spend.timestamp - first_spend.timestamp
    if days != 0:
        mounth_price = {'mounth_price': round(price / days.days * 30)}
    else:
        mounth_price = {'mounth_price': 0}
    return jsonify(mounth_price)

@bp.route('spends/move/car/<int:id>/yearprice', methods=['GET'])
@token_auth.login_required
def get_year_price(id):
    spends = CarSpend.query.filter(CarSpend.car_id==id).all()
    price = 0
    for s in spends:
        price += s.price * s.amount
    first_spend = spends[0]
    last_spend = spends[len(spends) - 1]
    days = last_spend.timestamp - first_spend.timestamp
    if days != 0:
        year_price = {'year_price': round(price / days.days * 365)}
    else:
        year_price = {'year_price': 0}
    return jsonify(year_price)

@bp.route('spends/move/car/start', methods=['GET'])
@token_auth.login_required
def get_start_info():
    # Username
    username = g.current_user.username
    
    # Cars list
    cars_list = []
    cars_query = Car.query.filter(Car.user_id == g.current_user.id)
    for car in cars_query:
        cars_list.append({'id': car.id, 'value': car.model.manufacturer + ' ' + car.model.model})
    cars_list = cars_list

    # Spend_types
    spend_types = CarSpendType.to_json()

    # Fuel consumption
    fuel_types = []
    types = CarSpendType.query.filter(CarSpendType.type.like('Бензин%')).all()
    for t in types:
        fuel_types.append(t.id)
    current_car = Car.query.filter(Car.user_id == g.current_user.id).first()
    car_id = current_car.id
    fuel_spends = CarSpend.query.filter(CarSpend.car_id==car_id, CarSpend.car_spend_type_id.in_(fuel_types)).all()
    amount = 0
    for i in range(len(fuel_spends) - 1):
        amount += fuel_spends[i].amount
    first_fuel_spend = fuel_spends[0]
    last_fuel_spend = fuel_spends[len(fuel_spends) - 1]
    trip = last_fuel_spend.trip - first_fuel_spend.trip
    if trip != 0:
        fuel_consumption = round((amount / trip * 100), 1)
    else:
        fuel_consumption = 0

    # Price of 1 km
    all_spends = CarSpend.query.filter(CarSpend.car_id==car_id).all()
    price = 0
    for s in all_spends:
        price += s.price * s.amount
    first_all_spend = all_spends[0]
    last_all_spend = all_spends[len(all_spends) - 1]
    trip_all = last_all_spend.trip - first_all_spend.trip
    if trip_all != 0:
        unit_price = round((price / trip_all), 2)
    else:
        unit_price = 0

    # Price of 1 mounth
    days = last_all_spend.timestamp - first_all_spend.timestamp
    if days != 0:
        mounth_price = round(price / days.days * 30)
    else:
        mounth_price = 0

    # Price of 1 year
    year_price = round(mounth_price / 30 * 365 )
    
    return jsonify({'username': username, 'cars_list': cars_list, 'spend_types': spend_types, 
                    'fuel_consumption': fuel_consumption, 'unit_price': unit_price, 
                    'mounth_price': mounth_price, 'year_price': year_price})