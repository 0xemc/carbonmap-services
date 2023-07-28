```python
from flask_sqlalchemy import SQLAlchemy
from app import db

class Result(db.Model):
    """
    Result Model for storing results
    """
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.String(60), nullable=False)

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return '<Result: {}>'.format(self.result)
```
