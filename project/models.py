from project.app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, default="Media", nullable=False)

    def __init__(self, title, text, priority=None):
        self.title = title
        self.text = text
        self.priority = priority    

    def __repr__(self):
        return f"<title {self.title}, priority {self.priority}>"
