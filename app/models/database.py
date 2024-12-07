from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# Mock user database
mock_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword")  # "testpassword" is the raw password
    }
}

def get_user(username: str):
    return mock_users_db.get(username)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
