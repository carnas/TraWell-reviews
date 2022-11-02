import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidIssuedAtError, InvalidSignatureError

from utils.variables import PUBLIC_KEY, ALGORITHMS, JWT_OPTIONS, ISSUER_CLAIM, AUDIENCE_CLAIM


def is_authorized(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
    except KeyError:
        return False

    try:
        jwt.decode(token, PUBLIC_KEY, algorithms=ALGORITHMS, issuer=ISSUER_CLAIM, audience=AUDIENCE_CLAIM,
                   options=JWT_OPTIONS)
        return True
    except (DecodeError, ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidIssuedAtError, InvalidSignatureError):
        return False

