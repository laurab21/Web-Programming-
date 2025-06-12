from passlib.context import CryptContext

# we define which algorithm to use to hash the passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# function to hash a plain password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# function to verify if a plain password matches the hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
