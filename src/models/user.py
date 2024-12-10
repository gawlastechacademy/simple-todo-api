from src.database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "is_admin": self.is_admin,
        }

    def is_administrator(self):
        print(self.is_admin)
        return self.is_admin == 1
