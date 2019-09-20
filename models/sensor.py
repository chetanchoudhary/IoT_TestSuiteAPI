from db import db


class SensorModel(db.Model):

    __tablename__ = "sensors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    cloud = db.Column(db.String(60))
    connection = db.Column(db.String(500))
    format = db.Column(db.String(10))
    timeInterval = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    minRange = db.Column(db.Integer)
    maxRange = db.Column(db.Integer)

    def __init__(self, name, cloud, connection, _format, timeInterval, frequency, minRange, maxRange):
        self.name = name
        self.cloud = cloud
        self.connection = connection
        self.format = _format
        self.timeInterval = timeInterval
        self.frequency = frequency
        self.minRange = minRange
        self.maxRange = maxRange

    def json(self):
        return {"name": self.name, "cloud": self.cloud, "connection": self.connection, "format": self.format, "timeInterval": self.timeInterval, "frequency": self.frequency, "minRange": self.minRange, "maxRange": self.maxRange}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
