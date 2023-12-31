#!/usr/bin/env python3
"""DB module
"""
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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Method to obtain the User object"""
        if not email or not hashed_password:
            return None
        if type(email) is not str or type(hashed_password) is not str:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session()
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Implement the find user method to return user obj
        raise invalid request if invalid arguments"""
        if not kwargs:
            raise InvalidRequestError
        else:
            user_obj = self._session.query(User).filter_by(**kwargs).first()
            if not user_obj:
                raise NoResultFound
        return user_obj

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user info for a certain user given the user id"""
        user_obj = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user_obj, key):
                raise ValueError
            else:
                setattr(user_obj, key, value)
        self._session.commit()
        return None
