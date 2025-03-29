from dataclasses import dataclass
from config.database import db

@dataclass
class UserEntity(db.Model):
    __tablename__ = "user_data"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    password: str = db.Column(db.String(255), nullable=False)
    hashed_password: str = db.Column(db.String(255), nullable=False)

    # 없어도 작동됨
    # def __repr__(self):
    #     return f"UserData(id={self.id}, username='{self.username}')"