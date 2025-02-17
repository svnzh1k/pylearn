import jwt
from datetime import datetime, timedelta
from typing import Dict

SECRET_KEY = "SECRET_KEY"
REFRESH_SECRET_KEY = "REFRESH_SECRET_KEY"

def generate_tokens(payload: Dict[str, any]) -> Dict[str, str]:
    access_payload = payload.copy()
    access_payload["exp"] = datetime.utcnow() + timedelta(seconds=50)

    refresh_payload = payload.copy()
    refresh_payload["exp"] = datetime.utcnow() + timedelta(days=7)

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET_KEY, algorithm="HS256")

    return {"access_token": access_token, "refresh_token": refresh_token}

def validate_token(token: str, is_refresh: bool = False) -> dict:
    secret = REFRESH_SECRET_KEY if is_refresh else SECRET_KEY
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        print("hello")
        raise ValueError("Invalid token")
    
    
