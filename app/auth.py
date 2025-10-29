from fastapi import HTTPException, Header
from jose import jwt, ExpiredSignatureError, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"

def verify_jwt_token(token: str = Header(...)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, os.getenv('SECRETKEY'), algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")