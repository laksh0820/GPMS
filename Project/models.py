from Project import db,app
from flask_login import UserMixin, LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    db.execute("""SELECT user_id, password, type
                  FROM users
                  WHERE user_id = %s;
               """, [id])
    return User(db.fetchall()[0])

class User(UserMixin):
    def __init__(self,data):
        self.user_id = data[0]
        self.password = data[1]
        self.type = data[2]
    
    def get_id(self):
        return self.user_id
