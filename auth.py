from passlib.hash import bcrypt


def hash_password(raw: str) -> str:
    return bcrypt.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return bcrypt.verify(raw, hashed)
