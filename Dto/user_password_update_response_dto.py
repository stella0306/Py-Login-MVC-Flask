from dataclasses import dataclass

@dataclass
class UserPasswordUpdateResponseDto:
    id: int
    username: str
    password: str
    hashed_password: str