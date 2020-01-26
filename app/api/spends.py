from app.api import bp
from app.api.auth import token_auth
from app.models import CarSpendType

@bp.route('/spends/move/car/types', methods=['GET'])
@token_auth.login_required
def get_car_spend_typs():
    return CarSpendType.to_json()