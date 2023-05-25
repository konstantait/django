import os
import hashlib
import binascii
from datetime import datetime
import random
import string


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


def make_random_key():
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(8))


def send_sms(phone, key):
    return phone, key


def store_key_hash_in_session(session, phone=None, secret_key=None):
    if not phone:
        phone = session.get('phone', None)
    if secret_key is None:
        secret_key = make_random_key()
    send_sms(phone, secret_key)
    session['phone'] = str(phone)
    session['phone_key_hash'] = hash_key(secret_key).decode('utf-8')
    session['phone_key_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # noqa
    session.save()
    return phone


def verify_key_hash_from_session(session, secret_key=None):
    phone = session.get('phone', None)
    secret_key_hash = session.get('phone_key_hash', None)
    secret_key_timestamp = session.get('phone_key_timestamp', None)
    if phone and secret_key_hash and secret_key_timestamp:
        secret_key_timestamp = datetime.strptime(secret_key_timestamp, '%Y-%m-%d %H:%M:%S') # noqa
        now_timestamp = datetime.now()
        is_valid = verify_key(secret_key, secret_key_hash.encode('utf-8'))
        is_valid &= (now_timestamp - secret_key_timestamp).total_seconds() < 1800 # noqa
        if not is_valid:
            return None
    return phone
