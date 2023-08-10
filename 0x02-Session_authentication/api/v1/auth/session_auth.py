#!/usr/bin/env python3
""" Session authentication """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ session auth class """
    user_id_by_session_id = dict({})

    def create_session(self, user_id: str = None) -> str:
        """ creates a session id """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ gets a user id based on session id """
        if session_id is None or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
