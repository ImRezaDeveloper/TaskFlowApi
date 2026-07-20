from fastapi.security import OAuth2PasswordBearer

oauth_schemes = OAuth2PasswordBearer(tokenUrl='auth/login')