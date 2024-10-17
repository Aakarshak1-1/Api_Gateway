import traceback
from functools import wraps

from flask import request
import requests as http_request
import requests



# def require_token(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # auth = request.headers.get('Authorization')
#         # if not auth:
#         #     return {'message': 'Unauthorized'}, 401
#         # print(auth.split(" ")[-1])
#         # jwt_access_token = auth.split(" ")[-1]
#         # if not jwt_access_token:
#         #     return {'message': 'Unauthorized'}, 401

#         # try:
#         #     headers = {'Authorization': f'Bearer {jwt_access_token}'}
#         #     url = 'http://auth_service:8080/public/auth/token/info'
#         #     resp = requests.get(url, headers=headers, timeout=5)
#         #     print(resp)
#         #     _resp = resp.json()

#         #     if resp.status_code != 200:
#         #         return _resp, resp.status_code

#         #     request.x_auth_user = _resp.get('data', {}).get('username')
#         #     request.x_auth_role = _resp.get('data', {}).get('role')

#             pass
#             return func(*args, **kwargs)
#         # except requests.exceptions.RequestException as e:
#         #     print(f"Error connecting to auth service: {str(e)}")
#         #     return {'message': 'Error connecting to authentication service'}, 503
#         # except Exception as e:
#         #     traceback.print_exc()
#         #     return {'message': 'Internal Server Error'}, 500
#     return wrapper

def require_permission(required_permission: None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = request.headers.get('X-Auth-Role')
            print(role)
            if not role:
                return {'message':'Forbidden'}, 403
            try:
                print("C-1")
                resp = http_request.get('http://auth_service:8080/public/auth/permissions',{'role':role})
                print(resp)
                _resp = resp.json()

                permissions = _resp.get('data',[])
                if required_permission in permissions:
                    return func(*args, **kwargs)
            except:
                traceback.print_exc()
                return {'message':'Internal Server Error'}, 500

            return {'message':'Forbidden'}, 403

        return wrapper
    return decorator
