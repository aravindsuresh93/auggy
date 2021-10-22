import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

ACCESS_TIME_LIMIT = 1
REFRESH_TIME_LIMIT = 2

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_payload(user_id, delta):
        return 

    def encode_token(self, user_id):
        access_payload = {
            'exp': datetime.utcnow() + timedelta(days=ACCESS_TIME_LIMIT),
            'iat': datetime.utcnow(),
            'sub': user_id
        }

        refresh_payload = {
            'exp': datetime.utcnow() + timedelta(days=REFRESH_TIME_LIMIT),
            'iat': datetime.utcnow(),
            'sub': user_id
        }

        access_token = jwt.encode(access_payload, self.secret, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, self.secret, algorithm='HS256')
        return access_token, refresh_token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
