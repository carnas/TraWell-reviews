from utils import user_utils


def is_authorized(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
    except KeyError:
        return False

    data = user_utils.decode_token(token)
    if 'error' in data.keys():
        return False

    return True
