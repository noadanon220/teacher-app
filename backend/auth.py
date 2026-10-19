import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "change-this-to-a-long-random-string"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def create_token(teacher_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(teacher_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    # Raises jwt.InvalidTokenError if the signature is wrong or the token expired
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])