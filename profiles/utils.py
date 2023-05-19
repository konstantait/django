import os
import hashlib
import binascii
from datetime import datetime


def hash_key(key):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    key_hash = hashlib.pbkdf2_hmac(
        'sha512',
        key.encode('utf-8'),
        salt,
        100000
    )
    key_hash = binascii.hexlify(key_hash)
    return salt + key_hash


def verify_key(provided_key, stored_key):
    stored_key = stored_key.decode('ascii')
    salt = stored_key[:64]
    stored_key = stored_key[64:]
    key_hash = hashlib.pbkdf2_hmac(
        'sha512',
        provided_key.encode('utf-8'),
        salt.encode('ascii'),
        100000)
    key_hash = binascii.hexlify(key_hash).decode('ascii')
    return key_hash == stored_key


def make_random_key(length=6, symbols='0123456789'):
    key = []
    for i in map(lambda x: int(len(symbols)*x/255.0), os.urandom(length)):
        key.append(symbols[i])
    return ''.join(key)


def send_sms(phone, key):
    print(phone, key)


def store_key_hash_in_session(request, phone=None):
    if not phone:
        phone = request.session.get('phone', None)
    secret_key = make_random_key()
    send_sms(phone, secret_key)
    request.session['phone'] = str(phone)
    request.session['phone_key_hash'] = hash_key(secret_key).decode('utf-8')
    request.session['phone_key_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # noqa
    return phone


def verify_key_hash_from_session(request, secret_key=None):
    phone = request.session.get('phone', None)
    secret_key_hash = request.session.get('phone_key_hash', None)
    secret_key_timestamp = request.session.get('phone_key_timestamp', None)
    if phone and secret_key_hash and secret_key_timestamp:
        secret_key_timestamp = datetime.strptime(secret_key_timestamp, '%Y-%m-%d %H:%M:%S') # noqa
        now_timestamp = datetime.now()
        is_valid = verify_key(secret_key, secret_key_hash.encode('utf-8'))
        is_valid &= (now_timestamp - secret_key_timestamp).total_seconds() < 60
        if not is_valid:
            return None
    return phone