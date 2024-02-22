#!/usr/bin/env python3
"""DB module
"""
from xml.dom import NotFoundErr
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
        if kwargs is None:
            raise InvalidRequestError

        query = self._session.query(User)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            query = query.filter(getattr(User, key) == value)

        user = query.first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes and commits changes to the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing attributes
                    to update (e.g., email="new_email@example.com").

        Raises:
            NoResultFound: If no user with the given ID is found.
            ValueError: If an invalid keyword argument is provided.
            StatementError: If a database-related error occurs during update.
        """
        if kwargs is None:
            return None

        rqrd_usr = self.find_user_by(id=8)
        key_cols = User.__table__.columns.keys()
        for k in kwargs:
            if k not in key_cols:
                raise ValueError

        for k, v in kwargs.items():
            setattr(rqrd_usr, k, v)

        self._session.commit()
