from .database import db, migrate, Base
from .oauth import oauth, config_oauth
from .mail import config_mail, send_mail
from .decorators import admin_required
