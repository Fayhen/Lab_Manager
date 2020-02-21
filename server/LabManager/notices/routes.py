import time
from flask import Blueprint, request, make_response, jsonify
from LabManager import db
from LabManager.dbModels import User, Notices
from LabManager.maSchemas import notice_schema, notices_schema
from LabManager.auth.utils import token_required


notices = Blueprint("notices", __name__)


@notices.route("/notices/all", methods=["GET"])
@token_required
def notices_all(current_user):
    notices = Notices.query.all()

    return jsonify(notices_schema.dump(notices))


@notices.route("/notices/add", methods=["POST"])
@token_required
def notices_add(current_user):
    title = request.json["title"]
    content = request.json["content"]
    archived = request.json["archived"]
    date = time.time()

    new_notice = Notices(
        title=title,
        content=content,
        archived=archived,
        user_id=current_user.id,
        date=date
        )

    db.session.add(new_notice)
    db.session.commit()

    return jsonify(notice_schema.dump(new_notice))


@notices.route("/notices/<int:id>", methods=["GET", "PUT", "DELETE"])
@token_required
def notices_ops(current_user, id):
    notice = Notices.query.filter_by(user_id=id).all()
    if notice is None:
        return make_response("No notices found for this user.", 404)

    if request.method == "GET":
        return jsonify(notices_schema.dump(notice))
    
    if request.method == "PUT":
        title = request.json["title"]
        content = request.json["content"]
        archived = request.json["archived"]
        user_id = request.json["user_id"]
        date = time.time()

        notice.title = title
        notice.content = content
        notice.archived = archived
        notice.user_id = user_id
        notice.date = date

        db.session.commit()

        return jsonify(notice_schema.dump(notice))
    
    if request.method == "DELETE":
        response = notice_schema.dump(notice)
        db.session.delete(notice)
        db.session.commit()

        return jsonify(response)
