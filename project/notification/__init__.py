from flask import Blueprint

notification = Blueprint('notificacao', __name__, template_folder='templates')

from .models import Notification, NotificationFriendRequest, NotificationType
from .controllers import notification_controller
from .services import NotificationService
from .repositories import NotificationRepository
from .exceptions import NotificationException
