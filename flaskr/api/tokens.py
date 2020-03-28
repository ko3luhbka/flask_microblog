from flask import jsonify, g
from flaskr.db import db
from flaskr.api import api_bp
from flaskr.api.auth import basic_auth, token_auth


@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_api_token()
    db.session.commit()
    return jsonify({'token': token})


@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_api_token()
    db.session.commit()
    return '', 204
