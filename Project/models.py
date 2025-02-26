from Project import db,app
from flask_login import UserMixin, LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db.execute("""SELECT *
                  FROM users
                  WHERE id = %s;
               """, [user_id])
    return User(db.fetchall()[0])

class User(UserMixin):
    def __init__(self,data):
        self.user_id = data[0]
        self.email = data[1]
        self.password = data[2]
        self.citizen_id = data[3]
        self.role = data[4]
    
    def get_id(self):
        return self.user_id
