from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tasks (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    done = db.Column(db.Boolean, nullable = False)
    label= db.Column(db.String(20), nullable = False)
    
    def __repr__(self):
        return "<User r%/>" % self.id

    def serialize(self): 
        return {
            "id": self.id,
            "done": self.done,
            "label": self.label
        }

    def serialize_username(self): 
        return {
            "id": self.id,
            "labek": self.label
        }

