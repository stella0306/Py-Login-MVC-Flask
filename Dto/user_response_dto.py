from dataclasses import dataclass

@dataclass
class UserResponseDto:
    id: int
    username: str
    password: str
    hashed_password: str