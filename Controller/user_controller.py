from flask import Blueprint, request, Response
import json
from Service.Impl.user_service_impl import  UserServiceImpl
from Dto.user_request_dto import UserRequestDto

user_bp = Blueprint(name="user", import_name=__name__)
user_service = UserServiceImpl()

@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
    result = user_service.create_user(UserRequestDto(**data))

    return Response(
        json.dumps(result if result else {}, ensure_ascii=False, indent=4),
        mimetype='application/json'
    ), 201


@user_bp.route("/get_all", methods=["POST"])
def get_users():
    data = request.get_json()

    # 인증 정보 확인 (username과 password가 'admin'일 때만 허용)
    username = data.get('username')
    password = data.get('password')
    
    if username == "admin" and password == "admin":
        results = user_service.get_users()
        result_dict = [result.__dict__ for result in results]

        return Response(
            json.dumps({"users": result_dict} if result_dict else {}, ensure_ascii=False, indent=4),
            mimetype='application/json'
        ), 200
    
    else:
        return Response(
            json.dumps({"message": "Unauthorized"}, ensure_ascii=False, indent=4), 
            mimetype='application/json'
        ), 401


@user_bp.route("/get", methods=["POST"])
def get_user():
    data = request.get_json()
    result = user_service.get_user(UserRequestDto(**data))
    
    return Response(
        json.dumps(result.__dict__ if result else {}, ensure_ascii=False, indent=4),
        mimetype='application/json'
    ), 200


@user_bp.route("/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    result = user_service.delete_user(UserRequestDto(**data))

    return Response(
        json.dumps(result if result else {}, ensure_ascii=False, indent=4),
        mimetype='application/json'
    ), 200