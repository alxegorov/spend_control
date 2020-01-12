from flask import g, jsonify
from app.api import bp
from app.api.auth import token_auth

@bp.route('/users/current', methods=['GET'])
@token_auth.login_required
def get_current_username():
    return jsonify({'username': g.current_user.username}) 