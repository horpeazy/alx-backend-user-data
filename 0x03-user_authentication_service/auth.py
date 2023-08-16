#!/usr/bin/env python3
""" auth module """
from sqlalchemy.orm.exc import NoResultFound
from user import User
from typing import TypeVar
from db import DB
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    hasheas a password and returns the result
    """
    if not password:
        return None
    password_hash = bcrypt.hashpw(password.encode(),
                                  bcrypt.gensalt())
    return password_hash


def _generate_uuid(self):
    """ generates an returns a uuid """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a user """
        if not email or not password:
            return None
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        password_hash = _hash_password(password)
        user = self._db.add_user(email, password_hash)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ validates credentials """
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        password_hash = user.hashed_password
        is_valid = bcrypt.checkpw(password.encode(), password_hash)
        return is_valid

    def create_session(self, email: str) -> str:
        """ creates a session id for a user """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar("User"):
        """ retrives the user with the session id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroys a user session """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the user password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        password_hash = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=password_hash,
                             reset_token=None)
