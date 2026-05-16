from project.app import db




class Post(db.Model):
    __tablename__ = "post"


    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(150), nullable=False)
    post_text = db.Column(db.String(500), nullable=False)
    post_priority = db.Column(
        db.String(20),
        nullable=False,
        default="Media"
    )


    def __init__(self, title, text, priority="Media"):
        self.post_title = title
        self.post_text = text
        self.post_priority = priority
