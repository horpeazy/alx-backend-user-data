#!/usr/bin/env python3
""" sessio auth module """
from flask import jsonify, request
from models.user import User
from api.v1.views import app_views
from models.user import User

@app_views.route("/auth_session/login", methods=["POST"],
                 strict_slashes=False)
def create_session() -> str:
    """ creates a session for a user """
    email = request.form.get("email")
    password = request.form.get("password")
    if not isinstance(email, str):
        return jsonify({"error": "email missing"}), 400
    if not isinstance(password, str):
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    cookie_name = os.environ.get("SESSION_NAME")
    res.set_cookie(cookie_name, session_id)
    return res

