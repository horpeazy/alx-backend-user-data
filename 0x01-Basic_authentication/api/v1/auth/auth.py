#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if an endpoint requires auth """
        if not path or not excluded_paths:
            return True
        if path[-1] == "/":
            path = path[:-1]
        for exc_path in excluded_paths:
            if exc_path[-1] == '/' or exc_path[-1] == '*':
                exc_path = exc_path[:-1]
            if re.match(rf"{exc_path}", path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ retrieves the authorization header """
        if not request:
            return None
        auth_header = request.headers.get("Authorization")
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user """
        return None
