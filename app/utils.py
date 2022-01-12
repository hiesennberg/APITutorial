from passlib.context import CryptContext
from passlib.utils.compat import str_to_bascii
from sqlalchemy.sql.expression import false, true


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def do_hash(password : str):
    
    return pwd_context.hash(password)


def verify(plain_password, hashed_password ):
    
    return pwd_context.verify(plain_password,hashed_password)