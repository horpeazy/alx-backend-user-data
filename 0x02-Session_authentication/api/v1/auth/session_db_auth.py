#!/usr/bin/env python3
""" session database authentication module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ sessiondbauth class """
    def create_session(self, user_id=None):
        """ creates a new usersession and store it in db """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ retrives a user_id based on session_id from db """
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not user_sessions or len(user_sessions) > 1:
            return None
        user_session = user_sessions[0]
        curr_time = datetime.utcnow()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = user_session.created_at + time_span
        if self.session_duration <= 0:
            return user_session.user_id
        if exp_time < curr_time:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys a user session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            users = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not users or len(users) > 1:
            return False
        user = users[0]
        user.remove()
        return True
