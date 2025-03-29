from dataclasses import dataclass

@dataclass
class UserRequestDto:
    username: str
    password: str