from Service.user_service import UserService
from Repository.user_repository import UserRepository
from Entity.user_entity import UserEntity
from werkzeug.security import generate_password_hash, check_password_hash
from Dto.user_request_dto import UserRequestDto
from Dto.user_response_dto import UserResponseDto

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
    def delete_user(self, user_request_dto):
        # 'admin' 계정은 삭제 금지
        if user_request_dto.username.lower() == "admin" or user_request_dto.password.lower() == "admin":
            return {"message": "Cannot delete 'admin' username or password"}
        
        user = UserRepository.find_by_username(user_request_dto.username)

        # 사용자 존재 여부 및 비밀번호 확인
        if not user or not check_password_hash(user.hashed_password, user_request_dto.password):
            return {"message": "Invalid credentials"}

        UserRepository.delete(user)
        return {"message": f"{user_request_dto.username} deleted successfully"}