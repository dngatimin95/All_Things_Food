import datetime as dt
from marshmallow import Schema, fields, ValidationError
# serialize and deserialize entities through the endpoints

class Locus(object):
    def __init__(self, id, name, type, priority, place_id, address, url):
        self._id = id
        self.name = name
        self.type = type
        self.priority = priority
        self.place_id = place_id
        self.address = address
        self.url = url
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<Locus(name={self.name!r})>'.format(self=self)

class LocusSchema(Schema):
    _id = fields.Str()
    name = fields.Str(required=True)
    type = fields.Str()
    priority = fields.Int()
    place_id = fields.Str(required=True)
    address = fields.Str()
    url = fields.URL()
    created_at = fields.Date()

