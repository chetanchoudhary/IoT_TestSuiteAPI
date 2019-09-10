from db import db


class SensorModel(db.Model):

    __tablename__ = "thingworx"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    broker = db.Column(db.String(60))
    topic = db.Column(db.String(60))
    appKey = db.Column(db.String(60))
    format = db.Column(db.String(10))
    timeInterval = db.Column(db.Integer)
    frequency = db.Column(db.Integer)

    def __init__(self, name, broker, topic, appKey, _format, timeInterval, frequency):
        self.name = name
        self.broker = broker
        self.topic = topic
        self.appKey = appKey
        self.format = _format
        self.timeInterval = timeInterval
        self.frequency = frequency

    def json(self):
        return {"name": self.name, "broker": self.broker, "topic": self.topic, "appKey": self.appKey, "format": self.format, "timeInterval": self.timeInterval, "frequency": self.frequency}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
