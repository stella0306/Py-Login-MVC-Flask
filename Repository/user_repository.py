from Entity.user_entity import UserEntity
from config.database import db

class UserRepository:
    @staticmethod
    def find_all():
        return UserEntity.query.all()
    
    @staticmethod
    def find_by_username(username: str) -> UserEntity | None:
        return UserEntity.query.filter_by(username=username).first()

    @staticmethod
    def save(user_entity: UserEntity):
        db.session.add(user_entity)
        db.session.commit()

    @staticmethod
    def delete(user_entity: UserEntity):
        user = UserEntity.query.filter_by(username=user_entity.username).first()
        if user:
            db.session.delete(user_entity)
            db.session.commit()