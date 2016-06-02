import cgi, os

import webapp2

import frbddn

class Robot(webapp2.RequestHandler):
    def get(self):
      txt = """User-agent: Googlebot
Allow: /

User-agent: *
Disallow: /
"""
      self.response.headers['Content-Type'] = 'plain/text'
      self.response.write(txt)

class Menu(webapp2.RequestHandler):
    def __init__(self, req, resp):
      self.initialize(req, resp)
      self.appdir = os.path.dirname (__file__)
      main = open(self.appdir + '/static/menu.json', 'r')
      self.main_tpl = main.read()
      main.close()

    def get(self):
      resp = self.response
      resp.headers ['Content-Type'] = 'application/json'
      resp.write (self.main)
      

class Root(webapp2.RequestHandler):
    def __init__(self, req, resp):
      self.initialize(req, resp)
      self.appdir = os.path.dirname (__file__)
      main = open(self.appdir + '/static/main.html', 'r')
      self.main_tpl = main.read()
      main.close()

    def getStaticData(self, fname):
            res = open(self.appdir + fname, 'r')
            resbody = res.read()
            res.close()
            return resbody

    def getContent(self):
        link = self.request.get ('link')
        req = self.request
        if 'resume' in link:
            return ('application/xhtml+xml',self.getStaticData('/static/resume.xhtml'))
        if 'sudoku-linux' in link:
            return ('text/html',self.getStaticData('/static/linsudoku.html'))
        if 'linsudoku' in link:
            return ('text/html',self.getStaticData('/static/linsudoku.html'))
            
        return ('text/html',self.main_tpl)

    def get(self):
      (mime,html) = self.getContent()
      resp = self.response
      resp.headers ['Content-Type'] = mime
      resp.write (html)

app = webapp2.WSGIApplication([
    ('/', Root),
    ('/menu.json', Menu),
    ('/robots.txt', Robot),
    ('/rest/v1/getCurrentBoard', frbddn.gameHandler),
], debug=False)

