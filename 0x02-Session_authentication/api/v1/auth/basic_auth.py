#!/usr/bin/env python3
""" basic auth module """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ basic auth class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extracts the base54 encoded authorization header """
        if not authorization_header or type(authorization_header) is not str:
            return None
        header_parts = authorization_header.split()
        if header_parts[0] != "Basic":
            return None
        return header_parts[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ decodes the base64 encoded authorization header """
        if not base64_authorization_header or \
                type(base64_authorization_header) is not str:
            return None
        try:
            base64_decode = base64.b64decode(base64_authorization_header)
            decoded_str = base64_decode.decode("utf-8")
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extracts user crendentials """
        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ gets a user from credentials """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user """
        auth_header = self.authorization_header(request)
        base64_auth_header = self.\
            extract_base64_authorization_header(auth_header)
        decoded_auth_header = self.\
            decode_base64_authorization_header(base64_auth_header)
        email, password = self.extract_user_credentials(decoded_auth_header)
        user = self.user_object_from_credentials(email, password)
        return user
