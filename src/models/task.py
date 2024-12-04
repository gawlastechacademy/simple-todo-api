from src.database import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "create_time": self.create_time,
            "due_date": self.due_date,
        }


def status_correct(status=str):
    return status.lower() == "to do" or status.lower() == "in progress" or status.lower() == "done"
