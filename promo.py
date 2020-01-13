from google.google.cloud import ndb

client = ndb.Client()


class Message(ndb.Model):
    promoID = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=False)
    msg = ndb.StringProperty(indexed=False)
    created = ndb.DateTimeProperty(auto_now=True,indexed=True)


def get_message_by_id(idx):
    pass
