from flask import jsonify, g
from flaskr.db import db
from flaskr.api import api_bp
from flaskr.api.auth import basic_auth


@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_api_token()
    db.session.commit()
    return jsonify({'token': token})
