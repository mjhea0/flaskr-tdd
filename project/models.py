from project.app import db

class Post(db.Model):
    priority = db.Column(db.String(10), nullable=False, default="Media")
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, title, text, priority="Media"):
        self.title = title
        self.text = text
        self.priority = priority

    def __repr__(self):
        return f"<title {self.title}>"