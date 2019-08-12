import os
import secrets
import jwt
from functools import wraps
from PIL import Image
from flask import request, jsonify
from LabManager import app
from LabManager.dbModels import User


def save_profile_picture(form_picture, image_path):
    """
    Logic to update account pictures. Used on the '/account'
    route. Generates random filename and concatenates to the
    original file extensions before saving it to the system.
    Also resizes the image using the Pillow Package. Returns
    the filename to be applied on the database.
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_filename = random_hex + file_ext
    pic_path = os.path.join(app.root_path, "static/profile_pics", pic_filename)
    
    if image_path != os.path.join(app.root_path, "static/profile_pics", "default.jpg"):
        os.remove(image_path)

    output_size = (125, 125)
    output_pic = Image.open(form_picture)
    output_pic.thumbnail(output_size)
    
    output_pic.save(pic_path)

    return pic_filename, os.path.join("static/profile_pics", pic_filename)

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
            invalid_msg["retrieved token"] = token
            invalid_msg["decoded token"] = data
            return jsonify(invalid_msg), 401

    return decorated
