from fastapi import Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWSError, jwt
from user import User
import mongo_actions
from pydantic import BaseModel
from constants import *
from mongo_actions import get_user
from fastapi.security import OAuth2PasswordBearer
from mongo_actions import clear_db

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uname: str or None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://127.0.0.1:8000/token')


def verify_pass(pl_pass, hash_pass):
    return pwd_context.verify(pl_pass, hash_pass)


def get_pass_hash(pwd):
    return pwd_context.hash(pwd)


def create_access_token(data, exp_delta: timedelta or None = None):
    to_enc = data.copy()
    if not exp_delta:
        exp = datetime.now() + exp_delta
    else:
        exp = datetime.now() + timedelta(minutes=15)

    to_enc.update({'exp': exp})
    encoded_jwt = jwt.encode(to_enc, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_curr_user(token: str = Depends(oauth2_scheme)):
    print(token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        u_name = payload.get('sub')
        if u_name is None:
            raise EXCEP_401_INVALID_CREDS
        token_data = TokenData(uname=u_name)

    except JWSError:
        raise EXCEP_401_INVALID_CREDS

    user = get_user(u_name=token_data.uname)
    if user is None:
        raise EXCEP_401_INVALID_CREDS

    return user


def auth_user(u_name, pwd):
    user = get_user(u_name=u_name)
    if not user:
        return False
    if not verify_pass(pwd, user.hash_pass):
        return False
    else:
        print('true')
    return user


def get_access_token(from_data):
    user = auth_user(from_data.username, from_data.password)
    if not user:
        raise EXCEP_401_INCORRECT_CREDS
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.u_name}, exp_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


"""def get_access_token_(username,pwd):
    user = auth_user(username,pwd)
    if not user:
        raise EXCEP_401_INCORRECT_CREDS
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.u_name}, exp_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}"""


def get_access_token_register(user):
    if not user:
        raise EXCEP_401_INCORRECT_CREDS
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.u_name}, exp_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


def register_user(u_name: str,
                  email: str,
                  f_name: str,
                  pwd: str):
    if mongo_actions.if_user_exists(u_name):
        raise EXCEP_400_ALREADY_EXISTS
    u = User(u_name=u_name, f_name=f_name, email=email, hash_pass=pwd_context.hash(pwd))
    mongo_actions.add_user(u)
    return u


if __name__ == "__main__":
    """from fastapi.testclient import TestClient
    import pymongo

    import CRUDactions

    client1 = pymongo.MongoClient("localhost:27017")
    db = client1.Market
    coll1 = db.Transactions
    coll2 = db.UsersTransactions
    coll3 = db.Users

    URL = 'http://127.0.0.1:8000'
    client = TestClient(CRUDactions.app, base_url=URL)"""
    import requests

    api_endpoint = "http://127.0.0.1:8000/ui"

    u = User(u_name='q', f_name='q', email='q', hash_pass=pwd_context.hash('q'))
    token = get_access_token_register(u)

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }

    response = requests.post(api_endpoint, headers=headers)

    if response.status_code == 200:
        print("Request successful")
        print(response.json())
    else:
        print("Request failed")
        print(response.json())
    """u = User(u_name='q', f_name='q', email='q', hash_pass=pwd_context.hash('q'))
    token = get_access_token_register(u)

    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }
    response = client.delete('/delet', headers=headers)
    print(response)"""
