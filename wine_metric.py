import cgi, webapp2

from google.appengine.ext import ndb

class MyUsers(ndb.Model):
    userID = ndb.StringProperty()
    license = ndb.IntegerProperty(indexed=False)
    lastAccess = ndb.DateProperty(auto_now=True)
    count = ndb.IntegerProperty(indexed=False)

class Metrics(webapp2.RequestHandler):
    def get(self):
        self.post()
        
    def post(self):
        id = self.request.get('googleAcc')
        lic = self.request.get('lic')
        if len(lic) < 1:
          lic = '0'
        
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
        
        self.response.headers['content-type'] = 'plain/text'
        self.response.write('\n')

application = webapp2.WSGIApplication([
    ('/store_user.php', Metrics),
], debug=False)

