import json
from functools import wraps
from urllib.request import urlopen

from flask import request, abort
from jose import jwt

AUTH0_DOMAIN = 'dev-dpx45agfqtrfqf7y.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'


class AuthError(Exception):

    """AuthError Exception

    A standardized way to communicate auth failure modes.

    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# get_token_auth_header() method
#     Attempts to get the header from the request,
#         and raise an AuthError if no header is present.
#     Attempts to split bearer and the token,
#         and raise an AuthError if the header is malformed
#     Returns the token part of the header.
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Authorization required.'
        }, 401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Invalid bearer token format.'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Bearer token required.'
        }, 401)

    return header_parts[1]


# check_permissions(permission, payload) method
#     @INPUTS
#         permission: string permission (i.e. 'post:movies')
#         payload: decoded jwt payload
#
#     Raises an AuthError if permissions are not included in the payload.
#         NOTE: check your RBAC settings in Auth0
#     Raises an AuthError if the requested permission string is not in the payload permissions array.
#     Return true otherwise
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Permission not found.'
        }, 403)

    return True


# verify_decode_jwt(token) method
#     @INPUTS
#         token: a json web token (string)
#
#     it should be an Auth0 token with key id (kid)
#     it should verify the token using Auth0 /.well-known/jwks.json
#     it should decode the payload from the token
#     it should validate the claims
#     return the decoded payload
#
#   !!NOTE urlopen has a common certificate error described here:
#   https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):
    # Get the public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose your key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Verify
    if not rsa_key:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Please check the audience and issuer.'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)


# @requires_auth(permission) decorator method
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
#
#     it should use the get_token_auth_header method to get the token
#     it should use the verify_decode_jwt method to decode the jwt
#     it should use the check_permissions method validate claims and check the requested permission
#     return the decorator which passes the decoded payload to the decorated method
def requires_auth(permissions=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permissions, payload)
            except AuthError as e:
                abort(e.status_code, e.error.get('description', 'Unknown error'))
            except Exception:
                abort(422, 'Error processing authentication.')
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
