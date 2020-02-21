import os
import secrets
import jwt
from functools import wraps
from flask import request, jsonify
from LabManager import app
from LabManager.dbModels import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        invalid_msg = {
            'message': 'Invalid token. Registration and / or authentication required.',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        notfound_msg = {
            'message': 'The logged user can no longer be found on the database. Please log in with a valid account.',
            'authenticated': False
        }

        auth_headers = request.headers.get("Authorization", "").split()
        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config["SECRET_KEY"])
            id = int(data["id"])
            current_user = User.query.filter_by(id=id).first()
            if not current_user:
                return jsonify(notfound_msg), 401

            return f(current_user, *args, **kwargs)

        
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401

        except jwt.InvalidTokenError:
            return jsonify(invalid_msg), 401
        
        except Exception as e:
            error_message = {
                'exeption': str(e),
                'authenticated': True
            }
            return jsonify(error_message), 500

    return decorated
