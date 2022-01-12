from jose import JWSError, jwt
from datetime import datetime, timedelta

from jose.exceptions import JWTError
from . import Schema
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer, oauth2
from .config import settings

# Secret_Key
#Algo : HS256
# Expritation_Time :

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

Secret_Key = settings.secret_key
Algorithm = settings.algorithm
Access_Token_Expire_Minutes = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=Access_Token_Expire_Minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, Secret_Key, algorithm=Algorithm)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token=token, algorithms=[Algorithm], key=Secret_Key)

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = Schema.TokenData(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", headers={'WWW-Authenticate':'Bearer'})
    
    return verify_access_token(token,credential_exception)
    
    