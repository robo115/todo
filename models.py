from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"{self.id}, {self.item}, {self.status}"
