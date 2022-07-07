from leapp.models import Model, fields
from leapp.topics import SystemFactsTopic


class ActiveVendorList(Model):
    topic = SystemFactsTopic

    data = fields.List(fields.String())
