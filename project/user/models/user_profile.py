from enum import Enum

import uuid

from core import Base
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from secrets import token_hex


class RoleEnum(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    GOD = 'god'


class UserProfile(UserMixin, Base):
    """
    A class representing a user's profile.

    Attributes:
        id (str): Unique identifier for the user's profile.
        alt_id (str): Alternative primary key used by Flask-Login.
        code (str): Unique code for user search. The system generates this code.
        user_id (int): Foreign key referencing the associated User entity.
        username (str): A unique username chosen by the user to identify themselves and log in to the system.
        pwd (str): Hashed password for user authentication.
        role (Role): User's role and access to the system's functionalities.
        visibility (Visibility): User profile's visibility level.
        profile_pic (str): URL to the user's profile picture.

    Relationships:
        user (User): A relationship to the User object representing the owner of the profile.
        sent_friend_requests (list[Friendship]): Friend requests sent by the user.
        received_friend_requests (list[Friendship]): Friend requests received by the user.
        notifications (List[Notification]): Notifications received by the user.
        sent_friend_notifications (List[NotificationFriendRequest]): Notifications of friend requests sent by the user.

    Methods:
        get_id() -> str: A method to get the alternative ID as the main ID of the user profile.

    Properties:
        friends (List[UserProfile]): List of the user's friends.
        pending_friend_requests (List[Friendship]): Incoming pending friend requests.
        pending_sent_requests (List[Friendship]): Outgoing pending friend requests.
    """
    __tablename__ = 'profiles'
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True, 
        default=str(uuid.uuid4()),
        comment='Primary key'
    )
    alt_id: Mapped[str] = mapped_column(
        String(36),
        unique=True, 
        default=str(uuid.uuid4()),
        comment='Alternative primary key used by Flask-Login'
    )
    code: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        default=lambda: token_hex(6),
        comment='Unique code for identifying users'
    )
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('users.id'), 
        unique=True,
        comment='Foreign key to the user table'
    )
    username: Mapped[str] = mapped_column(
        String(25), 
        unique=True, 
        nullable=False,
        comment='Username for identifying users'
    )
    pwd: Mapped[str] = mapped_column(
        String(250), 
        nullable=False,
        comment='Password for logging-in users'
    )
    #TODO: turn into enum
    visibility: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        default='public',
        comment='Visibility of the profile'
    )
    profile_pic: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
        default='/static/img/user.png',
        comment='Profile picture of the user'
    )
    role: Mapped[RoleEnum] = mapped_column(
        'RoleEnum', nullable=False, default=RoleEnum.USER,
        comment="User's role in the system."
    )
    supervisor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey('profiles.id'), nullable=True,
        comment="Supervisor's ID for student's users who want to suggest diets and workouts."
    )
    google_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=True,
        comment="Google ID for users who are using google login."
    )

    ##### Relationships #####

    user: Mapped['User'] = relationship(
        'User',
        back_populates='profile'
    )

    supervisor: Mapped['UserProfile'] = relationship('UserProfile', remote_side=[id], back_populates='supervised_students')

    supervised_students: Mapped[list['UserProfile']] = relationship('UserProfile', back_populates='supervisor', foreign_keys=[supervisor_id])

    sent_friend_requests: Mapped[list['Friendship']] = relationship(
        'Friendship',
        back_populates='sender',
        foreign_keys='[Friendship.sender_id]',
        cascade='all, delete-orphan'
    )
    received_friend_requests: Mapped[list['Friendship']] = relationship(
        'Friendship',
        back_populates='receiver',
        foreign_keys='[Friendship.receiver_id]',
        cascade='all, delete-orphan'
    )
    notifications: Mapped[list['Notification']] = relationship(
        'Notification',
        back_populates='receiver',
        foreign_keys='[Notification.receiver_id]',
        cascade='all, delete-orphan'
    )
    sent_friend_notifications: Mapped[list['NotificationFriendRequest']] = relationship(
        'NotificationFriendRequest',
        back_populates='sender',
        foreign_keys='[NotificationFriendRequest.sender_id]',
        cascade='all, delete-orphan'
    )

    majors: Mapped[list['UserMajor']] = relationship('UserMajor', back_populates='profile', cascade='all, delete-orphan')

    studied_majors: Mapped[list['UserMajor']] = relationship('UserMajor', primaryjoin="and_(UserProfile.id == "
                                                                                     "UserMajor.profile_id, "
                                                                                     "UserMajor.user_is == "
                                                                                     "'student')", viewonly=True)
    taught_majors: Mapped[list['UserMajor']] = relationship('UserMajor', primaryjoin="and_(UserProfile.id == "
                                                                                     "UserMajor.profile_id, "
                                                                                     "UserMajor.user_is == "
                                                                                     "'professor')", viewonly=True)

    posts: Mapped[list['Post']] = relationship('Post', back_populates='profile', cascade='all, delete-orphan')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='profile', cascade='all, delete-orphan')

    created_routines: Mapped[list['Routine']] = relationship('Routine', back_populates='creator', foreign_keys='[Routine.created_by]', cascade='all, delete-orphan')
    routines: Mapped[list['Routine']] = relationship('Routine', back_populates='receiver', foreign_keys='['
                                                                                                        'Routine.created_for]', cascade='all, delete-orphan')

    def get_id(self):
        """
        A method to get the alternative ID as the main ID of the user profile.

        Returns:
            str: The alternative ID of the user profile.
        """
        return self.alt_id

    @property
    def friends(self) -> list['UserProfile']:
        """
        A property to get the list of friends that belongs to the logged-in user.

        Returns:
            list['UserProfile']: The list of friends.
        """
        return [f.receiver for f in self.sent_friend_requests if f.status == 'accepted'] + \
            [f.sender for f in self.received_friend_requests if f.status == 'accepted']

    @property
    def pending_friend_requests(self) -> list['UserProfile']:
        """
        A property to get the list of pending friend requests received by the logged-in user.

        Returns:
            list['UserProfile']: The list of users who have sent friend requests to the logged-in user and have not been accepted yet.
        """
        return [f.sender for f in self.received_friend_requests if f.status == 'pending']

    @property
    def pending_sent_requests(self) -> list['UserProfile']:
        """
        A property to get the list of pending friend requests sent by the logged-in user.

        Returns:
            list['UserProfile']: The list of users who have received friend requests from the logged-in user and have not accepted yet.
        """
        return [f.receiver for f in self.sent_friend_requests if f.status == 'pending']

    @property
    def is_student(self) -> bool:
        """
        A property to determine if the user is a student based on their majors.

        Returns:
            bool: True if the user is a student, False otherwise.
        """
        return any(m.approved for m in self.studied_majors)

    @property
    def is_professor(self) -> bool:
        """
        A property to determine if the user is a professor based on their majors.

        Returns:
            bool: True if the user is a professor, False otherwise.
        """
        return any(m.approved for m in self.taught_majors)

    @property
    def created_workout_routines(self) -> list['Routine']:
        return [w for w in self.created_routines if w.type.value == 'workout']

    @property
    def created_meal_routines(self) -> list['Routine']:
        return [m for m in self.created_routines if m.type.value == 'dietary']

    @property
    def workout_routines(self) -> list['Routine']:
        return [w for w in self.routines if w.type.value == 'workout']

    @property
    def meal_routines(self) -> list['Routine']:
        return [m for m in self.routines if m.type.value == 'dietary']
