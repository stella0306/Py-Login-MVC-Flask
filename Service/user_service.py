from abc import ABC, abstractmethod
from Dto.user_request_dto import UserRequestDto
from Dto.user_password_update_request_dto import UserPasswordUpdateRequestDto

class UserService(ABC):
    # 사용자 생성
    @abstractmethod
    def create_user(self, user_request_dto: UserRequestDto):
        pass

    # 모든 사용자 가져오기
    @abstractmethod
    def get_users(self):
        pass

    # 특정 사용자 가져오기
    @abstractmethod
    def get_user(self, user_request_dto: UserRequestDto):
        pass

    # 사용자 삭제
    @abstractmethod
    def delete_user(self, user_request_dto: UserRequestDto):
        pass

    # 비밀번호 변경
    @abstractmethod
    def change_password(self, user_password_update_request_dto: UserPasswordUpdateRequestDto):
        pass