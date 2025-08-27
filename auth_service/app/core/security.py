import datetime as dt
import jwt
from passlib.hash import pbkdf2_sha256

# Password hashing helpers
def hash_password(plain: str) -> str:
    return pbkdf2_sha256.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)

# JWT creation
def create_access_token(*, sub: str, expires_minutes: int, secret: str, algorithm: str) -> str:
    now = dt.datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": now,
        "exp": now + dt.timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, secret, algorithm=algorithm)
