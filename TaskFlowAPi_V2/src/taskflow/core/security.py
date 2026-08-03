from pwdlib import PasswordHash

# pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
password_hash = PasswordHash.recommended()


def hash_pwd(plainPassword: str):
    return password_hash.hash(plainPassword)


def verify_pwd(plainPassword: str, hashedPassword: str) -> bool:
    return password_hash.verify(plainPassword, hashedPassword)
