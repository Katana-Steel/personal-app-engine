from google.cloud import ndb

client = ndb.Client()


class MyUsers(ndb.Model):
    userID = ndb.StringProperty()
    license = ndb.IntegerProperty(indexed=False)
    lastAccess = ndb.DateProperty(auto_now=True)
    count = ndb.IntegerProperty(indexed=False)


def store_user(id, lic):
        with client.context():
          try:
            user = MyUsers.query(MyUsers.userID == id).fetch(1)
            user[0].license = int(lic)
            user[0].count += 1
            user[0].put()
          except:
            newUser = MyUsers()
            newUser.userID = id
            newUser.license = int(lic)
            newUser.count = 1
            newUser.put()
        return ''

