from flask import Blueprint, request, Response
import json
from Service.Impl.user_service_impl import  UserServiceImpl
from Dto.user_request_dto import UserRequestDto
from Dto.user_response_dto import UserResponseDto
from Dto.user_password_update_request_dto import UserPasswordUpdateRequestDto
from Dto.user_password_update_response_dto import UserPasswordUpdateResponseDto

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
    
    # DTO를 dict 형태로 변환
    result = result.__dict__ if isinstance(result, UserResponseDto) else result # 객체의 속성을 딕셔너리로 변환

    return Response(
        json.dumps(result if result else {}, ensure_ascii=False, indent=4),
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



@user_bp.route("/change_password", methods=["POST"])
def change_password():
    data = request.get_json()
    result = user_service.change_password(UserPasswordUpdateRequestDto(**data))
    
    # DTO를 dict 형태로 변환
    result = result.__dict__ if isinstance(result, UserPasswordUpdateResponseDto) else result # 객체의 속성을 딕셔너리로 변환

    return Response(
        json.dumps(result if result else {}, ensure_ascii=False, indent=4),
        mimetype='application/json'
    ), 200