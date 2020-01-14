from google.cloud import ndb
from hashlib import sha224

client = ndb.Client()


class Message(ndb.Model):
    promoID = ndb.StringProperty()
    title = ndb.StringProperty()
    msg = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now=True, indexed=True)


def generate_id(title):
    check = sha224(title.encode())
    genid = sha224(check.digest())
    check.update(genid.digest())
    genid.update(check.digest())
    check.update(genid.digest())
    genid.update(check.digest())
    return genid.hexdigest()[0:16]


def store_message(title, msg):
    with client.context():
        m = Message()
        m.title = title
        m.msg = msg
        m.promoID = generate_id(title)
        m.put()
        return m.promoID


def get_message_by_id(idx):
    with client.context():
        try:
            m = Message.query(Message.promoID == idx)
            return (m[0].title, m[0].msg)
        except Exception:
            return None
