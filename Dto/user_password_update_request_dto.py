from dataclasses import dataclass

@dataclass
class UserPasswordUpdateRequestDto:
    username: str
    old_password: str
    new_password: str