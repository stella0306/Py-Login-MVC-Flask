from Service.user_service import UserService
from Repository.user_repository import UserRepository
from Entity.user_entity import UserEntity
from werkzeug.security import generate_password_hash, check_password_hash
from Dto.user_request_dto import UserRequestDto
from Dto.user_response_dto import UserResponseDto
from Dto.user_password_update_request_dto import UserPasswordUpdateRequestDto
from Dto.user_password_update_response_dto import UserPasswordUpdateResponseDto

class UserServiceImpl(UserService):
    # 사용자 생성
    def create_user(self, user_request_dto: UserRequestDto):
        # 'admin' username이나 password가 들어오면 생성 금지
        if user_request_dto.username.lower() == "admin" or user_request_dto.password.lower() == "admin":
            return {"message": "Cannot create 'admin' username or password"}

         # 이미 존재하는 사용자 확인
        if UserRepository.find_by_username(user_request_dto.username):
            return {"message": "Username already exists"}
        
        hashed_pw = generate_password_hash(user_request_dto.password)
        new_user = UserEntity(username=user_request_dto.username, password=user_request_dto.password, hashed_password=hashed_pw)
        UserRepository.save(new_user)
        return {"message": f"{user_request_dto.username} created successfully"}
    
    # 모든 사용자 가져오기
    def get_users(self):
        # 모든 사용자 데이터를 반환하는 로직
        users = UserRepository.find_all()
        if not users:
            return {"message": "No users found"}
        
        # 반환할 사용자 정보만 필요한 데이터를 포함하여 반환
        user_list = [UserResponseDto(id=user.id, username=user.username, password=user.password, hashed_password=user.hashed_password) for user in users]
        return user_list
    
    # 특정 사용자 가져오기
    def get_user(self, user_request_dto: UserRequestDto):
        user = UserRepository.find_by_username(user_request_dto.username)

        # 사용자 존재 여부 및 비밀번호 확인
        if not user or not check_password_hash(user.hashed_password, user_request_dto.password):
            return {"message": "Invalid credentials"}

        return UserResponseDto(id=user.id, username=user.username, password=user.password, hashed_password=user.hashed_password)
    
    # 사용자 삭제
    def delete_user(self, user_request_dto: UserRequestDto):
        # 'admin' 계정은 삭제 금지
        if user_request_dto.username.lower() == "admin" or user_request_dto.password.lower() == "admin":
            return {"message": "Cannot delete 'admin' username or password"}
        
        user = UserRepository.find_by_username(user_request_dto.username)

        # 사용자 존재 여부 및 비밀번호 확인
        if not user or not check_password_hash(user.hashed_password, user_request_dto.password):
            return {"message": "Invalid credentials"}

        UserRepository.delete(user)
        return {"message": f"{user_request_dto.username} deleted successfully"}
    
    # 비밀번호 변경
    def change_password(self, user_password_update_request_dto: UserPasswordUpdateRequestDto):
        user = UserRepository.find_by_username(user_password_update_request_dto.username)
        if not user:
            return {"message": "User not found"}, 404
        
        if not check_password_hash(user.hashed_password, user_password_update_request_dto.old_password):
            return {"message": "Incorrect old password"}, 400

        # 'admin' 계정 또는 비밀번호 변경 제한
        if user.username.lower() == "admin" or user_password_update_request_dto.new_password.lower() == "admin":
            return {"message": "Cannot change password for 'admin' user or set password as 'admin'"}, 403

        # 새로운 비밀번호가 현재 비밀번호와 동일한지 확인
        if check_password_hash(user.hashed_password, user_password_update_request_dto.new_password):
            return {"message": "New password cannot be the same as the current password"}, 400


        # 업데이트
        change_hashed_pw = generate_password_hash(user_password_update_request_dto.new_password)

        user.password = user_password_update_request_dto.new_password
        user.hashed_password = change_hashed_pw
        UserRepository.save(user)

        return UserPasswordUpdateResponseDto(id=user.id, username=user_password_update_request_dto.username, password=user_password_update_request_dto.new_password, hashed_password=change_hashed_pw)