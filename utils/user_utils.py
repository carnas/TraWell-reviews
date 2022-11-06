import os

import jwt
from jwt import DecodeError, ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidIssuedAtError, \
    InvalidSignatureError


def decode_token(token: str):
    try:
        public_key = f"""-----BEGIN RSA PUBLIC KEY-----\n{os.environ.get("TOKEN_KEY")}\n-----END RSA PUBLIC KEY-----"""
        issuer_claim = os.environ.get("ISSUER_CLAIM")
        data = jwt.decode(token, public_key, algorithms=['RS256'], issuer=issuer_claim,
                          audience='account', options={'verify_signature': True,
                                                       'verify_exp': True,
                                                       'verify_iss': True,
                                                       'verify_iat': True,
                                                       'verify_aud': True})
        return data
    except (DecodeError, ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidIssuedAtError,
            InvalidSignatureError):
        return {'error': 'Decoding failed'}


def was_rated_driver(rated_user_type: str):
    if rated_user_type == 'driver':
        return True
    elif rated_user_type == 'passenger':
        return False
    else:
        return None
