#!/usr/bin/env python3
""" user session models module """
from models.base import Base


class UserSession(Base):
    """ usersession class """
    def __init__(self, *args: list, **kwargs: dict):
        """ initialize the class """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
