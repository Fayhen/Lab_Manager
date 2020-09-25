import os
from flask import Blueprint, jsonify, send_from_directory
from LabManager import app

file_transfer = Blueprint("file_transfer", __name__)


@file_transfer.route("/get_images/<path:path>")
def get_image(path):
  folder, name = path.split("/")
  parsed_path = os.path.join(folder, name)

  return send_from_directory(app.config["IMG_DIR"], parsed_path)
