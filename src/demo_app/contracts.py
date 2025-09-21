from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

Username = Annotated[str, Field(min_length=3, max_length=20)]
Role = Literal["admin", "staff", "guest"]


class User(BaseModel):
    id: int
    username: Username
    email: Annotated[str, Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")]
    role: Role = "guest"

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("username must not contain spaces")
        return v


def validate_user(data: dict[str, Any]) -> User:
    """Validate inbound data into a User contract, raising ValidationError on failure."""
    # v2: prefer model_validate for dict-like inputs
    return User.model_validate(data)


class PasswordPair(BaseModel):
    password1: str
    password2: str

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordPair":
        if self.password1 != self.password2:
            raise ValueError("passwords do not match")
        return self


__all__ = [
    "User",
    "validate_user",
    "ValidationError",
    "PasswordPair",
]
