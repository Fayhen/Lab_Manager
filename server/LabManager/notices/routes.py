from datetime import datetime
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

    return jsonify(notices_schema.dump(notices).data)


@notices.route("/notices/add", methods=["POST"])
@token_required
def notices_add(current_user):
    title = request.json["title"]
    content = request.json["content"]
    archived = request.json["archived"]
    user_id = request.json["user_id"]
    date = datetime.utcnow()

    new_notice = Notices(title=title, content=content, archived=archived, user_id=user_id, date=date)

    db.session.add(new_notice)
    db.session.commit()

    return jsonify(notice_schema.dump(new_notice).data)


@notices.route("/notices/<int:id>", methods=["GET"])
@token_required
def notices_fetch(current_user, id):
    notice = Notices.query.get(id)
    if notice is None:
        return make_response("Notice entry does not exist.", 404)

    return jsonify(notice_schema.dump(notice).data)

  
@notices.route("/notices/user/<int:id>", methods=["GET"])
@token_required
def notices_user(current_user, id):
    notices = Notices.query.filter_by(user_id=id).all()
    if notices is None:
        return make_response("No notices found for this user.", 404)

    return jsonify(notices_schema.dump(notices).data)


@notices.route("/notices/update/<int:id>", methods=["PUT"])
@token_required
def notices_update(current_user, id):
    notice = Notices.query.get(id)
    if notice is None:
        return make_response("Notice entry does not exist.", 404)

    title = request.json["title"]
    content = request.json["content"]
    archived = request.json["archived"]
    user_id = request.json["user_id"]
    date = datetime.utcnow()

    notice.title = title
    notice.content = content
    notice.archived = archived
    notice.user_id = user_id
    notice.date = date

    db.session.commit()

    return jsonify(notice_schema.dump(notice).data)


@notices.route("/notices/delete/<int:id>", methods=["DELETE"])
@token_required
def notices_delete(current_user, id):
    notice = Notices.query.get(id)
    if notice is None:
        return make_response("Notice entry does not exist.", 404)

    response = notice_schema.dump(notice).data
    db.session.delete(notice)
    db.session.commit()

    return jsonify(response)