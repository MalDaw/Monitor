
from database.models import Alert, User
import datetime


class AlertLogger:
    def __init__(self, log_file='alerts.log'):
        self.log_file = log_file

    def log_alert(self, message, source=None, user=None):
        timestamp = datetime.datetime.now()
        full_msg = f"[{timestamp}] [User: {user}] [{message}]"
        if isinstance(user, tuple):
            user = user[1]
        db_user = User.get_or_create(name=user)[0] if user else None

        with open(self.log_file, 'a') as f:
            f.write(full_msg + '\n')

        Alert.create(
            timestampField=timestamp,
            message=message,
            source=source,
            user=db_user
        )

        print(full_msg)
