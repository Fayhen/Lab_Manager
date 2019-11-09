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
        internals_msg = {
            'message': 'Server-side error. Please seek shelter and contact support.',
            'authenticated': False
        }

        auth_headers = request.headers.get("Authorization", "").split()
        if len(auth_headers) != 2:
            invalid_msg["in"] = "line 50"
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config["SECRET_KEY"])
            id = int(data["id"])
            current_user = User.query.filter_by(id=id).first()
            if not current_user:
                raise RuntimeError('User not found')

            return f(current_user, *args, **kwargs)

        except RuntimeError:
            return jsonify(internals_msg), 500

        except TypeError:
            return jsonify(internals_msg), 500
        
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401

        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            invalid_msg["in"] = "line 74"
            invalid_msg["exception"] = str(e)
            return jsonify(invalid_msg), 401

    return decorated
