from pydantic import Field, BaseModel

class SignupRequest(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    password: str = Field(min_length=6)