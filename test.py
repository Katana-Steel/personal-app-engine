import cgi, webapp2, os

appdir = os.path.dirname (__file__)

class Root (webapp2.RequestHandler):
  def __init__(self, req, resp):
    self.initialize(req, resp)
    self.appdir = os.path.dirname (__file__)
  def get (self):
    resp = self.response
    resp.headers ['Content-Type'] = 'text/html'
    index = open (self. appdir + '/static/test.html', 'r')
    resp.write (index.read ())
    index.close ()

application = webapp2.WSGIApplication ([
  ('/test/', Root),
])
