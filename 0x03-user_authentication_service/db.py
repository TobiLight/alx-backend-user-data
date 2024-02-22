#!/usr/bin/env python3
"""DB module
"""
from xml.dom import NotFoundErr
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


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
        """
        Adds a new user to the database and returns the User object.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by filtering on multiple keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing attributes
                    to filter by (e.g., email="john@example.com").

        Returns:
            User: The first matching user object, or raises an exception.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If invalid keyword arguments are provided.
        """
        if not kwargs:
            raise InvalidRequestError()

        query = self._session.query(User)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
            query = query.filter(getattr(User, key) == value)

        user = query.first()

        if user is None:
            raise NoResultFound()

        return user
