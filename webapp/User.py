class User():
    """A console user

    Attributes:
        username    Username
        password    User Password
        role        User role, define access privileges.
                    1- Admin privileges
                    2- Full Viewing privileges
                    3- Limited Viewing privileges

    """

    def __init__(self, username, password='', role=''):
        self.username = username
        self.password = password
        self.role = role
        self.authenticated = False

    def is_active(self):
        """Flask-login - all users are active
        """
        return True

    def get_id(self):
        """Flask-login - use username as id
        """
        return self.username

    def is_authenticated(self):
        """Flask-login - authentication flag
        """
        return True

    def is_anonymous(self):
        """Flask-login - anonymous users aren't supported
        """
        return False




