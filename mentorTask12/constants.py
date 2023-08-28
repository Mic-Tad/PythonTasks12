from fastapi import FastAPI, Request, HTTPException, status, Form

# exceptions
EXCEP_400_ALREADY_EXISTS = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                         detail='uname is already in db', headers={'www-auth': 'Bearer'})
EXCEP_400_TR_ALREADY_EXISTS = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                         detail='transaction is already in db', headers={'www-auth': 'Bearer'})
EXCEP_401_INCORRECT_CREDS = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='incorrect uname or pass', headers={'www-auth': 'Bearer'})
EXCEP_401_INVALID_CREDS = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not valid creds',
                                        headers={'www-auth': 'Bearer'})
EXCEP_400_WRONG_USER = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail='Wrong user. You cant interact with others transactions',
                                     headers={'www-auth': 'Bearer'})
EXCEP_404_USER_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                         detail='uname is not in db')
# password encryption


SECRET_KEY = 'dbce5e2f32b49dca856c6d01cd76391a45bfbc91943011c1f4cd145a992d6da6'
ALGORITHM = 'HS256'
# time
ACCESS_TOKEN_EXPIRE_MINUTES = 30
