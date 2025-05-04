class UserProfileException(Exception):
    def __init__(self, message):
        super(UserProfileException, self).__init__(message)
        self.message = message
