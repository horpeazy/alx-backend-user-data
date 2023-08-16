#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Dict, Any
from user import Base, User
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the db with the given email and hashed password.

        Args:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: A User object representing the new user.
        """
        # Create new user
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            return None
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """ finds a user by the arbitrary inputs """
        if len(kwargs) == 0:
            raise NoResultFound
        try:
            query = self._session.query(User).filter_by(**kwargs)
            user = query.first()
            if not user:
                raise NoResultFound
            return user
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """ updates the user """
        if not user_id:
            return None
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            attr = getattr(User, key, None)
            if attr is None:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
