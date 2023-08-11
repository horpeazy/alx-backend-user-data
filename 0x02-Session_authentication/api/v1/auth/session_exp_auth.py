#!/usr/bin/env python3
""" session expire auth module """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
import os


class SessionExpAuth(SessionAuth):
    """ sessionexpauth class """
    def __init__(self):
        """ instantiate the class """
        super(SessionExpAuth, self).__init__()
        try:
            self.session_duration = int(os.environ.get("SESSION_DURATION"))
        except TypeError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates a user session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ grabs the user_id given a session_id """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None
        return session_dictionary.get("user_id")
