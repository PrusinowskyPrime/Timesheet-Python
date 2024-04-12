from fastapi.security import OAuth2PasswordBearer

from app.settings.auth import LOGIN_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_URL)
