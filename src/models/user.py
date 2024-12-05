from src.database import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "admin": self.admin,
        }
