from werkzeug.security import generate_password_hash, check_password_hash

from webapp import login

from webapp.DBManager import DBManager
from webapp.const import SQL_DB
from webapp.User import User


@login.user_loader
def load_user(id):
    db = DBManager()
    db.open()
    users = db.select('SELECT * FROM users WHERE username=?',(id,))

    if len(users) > 0:
        role = users[0][3]

        user = User(id,role=role)
        return user
    else:
        return None

class UsersManager():
    """Users managemant interface

    Attributes:
        user (User)     The user object
        db (DBManager)  The database manager object
    """

    def __init__(self, user=None):
        self.user = user
        self.db = DBManager()

    def check(self):
        """Check if user/pwd are in DB

        Return:
            result (boolean)
        """

        self.db.open()
        results = self.db.select('SELECT * FROM users WHERE username=?',(self.user.username,))

        if len(results) > 0:
            if check_password_hash(results[0][2], self.user.password):
                return True

        return False


    def add(self):
        """Add a new user

        Return:
            (result (boolean), errors (string))
        """
        self.db.open()
        return self.db.insert('INSERT INTO users (username,password,role) VALUES (?,?,?)', (self.user.username,generate_password_hash(self.user.password),self.user.role))


    def remove(self):
        """Remove a user

        Return:
            (result (boolean), errors (string))
        """

        self.db.open()
        return self.db.delete('DELETE FROM users WHERE username=?',(self.user.username,))

    def update(self):
        """Update user details

        Return:
            (result (boolean), errors (string))
        """

        result = True
        error = ""


        if self.user.password != '':
            self.db.open()
            result, error = self.db.update('UPDATE users SET password=? WHERE username=?', (generate_password_hash(self.user.password), self.user.username))
            if not result:
                return (result,error)

        if self.user.role != '':
            self.db.open()
            result,error = self.db.update('UPDATE users SET role=? WHERE username=?', (self.user.role, self.user.username))
            if not result:
                return (result,error)


        return (result,error)

    def getAll(self):
        """Get all users in DB

        Return:
            users (Array[User])
        """

        users_list = []

        self.db.open()
        results = self.db.select('SELECT username, role FROM users',())

        for result in results:
            tmp_user = User(username = result[0],
                            role = result[1])
            users_list.append(tmp_user)

        return users_list
