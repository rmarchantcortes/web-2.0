import random
import hashlib
from datetime import(
    datetime, 
    timedelta
)
from flask import(
    request,
    session
)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_AGE = timedelta(hours=4)

def get_new_salt():    
    chars=[]
    for i in range(8):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)

def get_hash(password, salt):
    return hashlib.sha224(b""+password+salt).hexdigest()

def set_token(user_id, perfil):
    return {'id': user_id, 'perfil': perfil, 'datetime': datetime.now()}

def validate(token):
    if 'token' in session and datetime.now() - session['token']['datetime'] <= MAX_AGE:
        return True
    elif 'token' in session and datetime.now() - session['token']['datetime'] > MAX_AGE:
        unset_session()
        return False
    else:
        return False
    
def set_session(token):
    session['token'] = token

def unset_session():
    if 'token' in session:
        del session['token']

def get_token():
    if 'token' in session:
        return session['token']
    return False
    
def get_user_id(token):
    return token['id']

def get_perfil(token):
    return token['perfil']