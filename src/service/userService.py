import bcrypt

from datetime import datetime, timedelta

from fastapi import HTTPException

from jose import jwt

from config import Config


class UserService:
    encoding: str = "UTF-8"
    secret: str = Config.get_secret_key()
    algorithm: str = "HS256"
    access_expires = timedelta(hours=1)
    refresh_expires = timedelta(days=1)
    

    def hash_password(self, password: str) -> str | None:
        if not password:
            return None
        hashed_password: bytes = bcrypt.hashpw(
            password=password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )
    
    def encode_token(self, sub: str, expires: timedelta) -> str:
        return jwt.encode(
            {
                "exp": datetime.now() + expires,
                "iat": datetime.now(),
                "sub": sub,
            },
            self.secret,
            self.algorithm,
        )
    
    def decode_token(self, token: str):
        try:
            payload: dict = jwt.decode(token=token, key=self.secret, algorithms=[self.algorithm])
            # expire check 생략
            return payload["sub"]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=401, detail="Invalid Token")
        # except jwt.ExpiredSignatureError:
        #     raise HTTPException(status_code=401, detail="Token Expired")
        # except jwt.InvalidTokenError:
        #     raise HTTPException(status_code=401, detail="Invalid Token")
        
    def create_access_token(self, user):
        sub = str(user.id)
        return self.encode_token(sub, self.access_expires)
    
    def create_refresh_token(self, user):
        sub = f"{user.id}.refresh"
        return self.encode_token(sub, self.refresh_expires)