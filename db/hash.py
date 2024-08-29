from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Va prendre en entrée un mdp en txt clair et va le retourner
# en version hachée avec bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# On va prendre un mdp en clair et un mdp haché puis retourner True si les
# deux matchent, sinon on retournera False
def password_verification(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
