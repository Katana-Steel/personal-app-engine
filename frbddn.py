
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users

import webapp2,json,random

tiles = [
  {'name': 'Helicopter Landing' ,'state':0, 'base':'heliport'},
  {'name': 'Treasure E Zone 1' ,'state':0, 'base':'earth1'},
  {'name': 'Treasure F Zone 1' ,'state':0, 'base':'fire1'},
  {'name': 'Treasure W Zone 1' ,'state':0, 'base':'wind1'},
  {'name': 'Treasure M Zone 1' ,'state':0, 'base':'metal1'},
  {'name': 'Treasure E Zone 2' ,'state':0, 'base':'earth2'},
  {'name': 'Treasure F Zone 2' ,'state':0, 'base':'fire2'},
  {'name': 'Treasure W Zone 2' ,'state':0, 'base':'wind2'},
  {'name': 'Treasure M Zone 2' ,'state':0, 'base':'metal2'},
  {'name': 'Player1 Gate' ,'state':0, 'base':'gate1'},
  {'name': 'Player2 Gate' ,'state':0, 'base':'gate2'},
  {'name': 'Player3 Gate' ,'state':0, 'base':'gate3'},
  {'name': 'Player4 Gate' ,'state':0, 'base':'gate4'},
  {'name': 'Player5 Gate' ,'state':0, 'base':'gate5'},
  {'name': 'Plain Zone 1' ,'state':0, 'base':'plain1'},
  {'name': 'Plain Zone 2' ,'state':0, 'base':'plain2'},
  {'name': 'Plain Zone 3' ,'state':0, 'base':'plain3'},
  {'name': 'Marsh Zone 1' ,'state':0, 'base':'marsh1'},
  {'name': 'Marsh Zone 2' ,'state':0, 'base':'marsh2'},
  {'name': 'Marsh Zone 3' ,'state':0, 'base':'march3'},
  {'name': 'Hills Zone 1' ,'state':0, 'base':'hills1'},
  {'name': 'Hills Zone 2' ,'state':0, 'base':'hills2'},
  {'name': 'Hills Zone 3' ,'state':0, 'base':'hills3'},
  {'name': 'Mount Zone N' ,'state':0, 'base':'mount1'},
  {'name': 'Mount Zone S' ,'state':0, 'base':'mount2'},
  {'name': 'Mount Zone E' ,'state':0, 'base':'mount3'},
  {'name': 'Mount Zone W' ,'state':0, 'base':'mount4'},
]

def helo():
  return ('helo-lift')

def goal(t):
  return('{0}-treasure'.format(t))

def sandbag():
  return( 'shore-up')

def flood():
  return('draw-flood')

treasure = [
  {'name': 'Helicopter Lift','base':'heliport','effect': helo() },
  {'name': 'Helicopter Lift','base':'heliport','effect': helo() },
  {'name': 'Helicopter Lift','base':'heliport','effect': helo() },
  {'name': 'Treasure E', 'base':'earth', 'effect': goal('earth')},
  {'name': 'Treasure E', 'base':'earth', 'effect': goal('earth')},
  {'name': 'Treasure E', 'base':'earth', 'effect': goal('earth')},
  {'name': 'Treasure E', 'base':'earth', 'effect': goal('earth')},
  {'name': 'Treasure E', 'base':'earth', 'effect': goal('earth')},
  {'name': 'Treasure F', 'base':'fire',  'effect': goal('fire')},
  {'name': 'Treasure F', 'base':'fire',  'effect': goal('fire')},
  {'name': 'Treasure F', 'base':'fire',  'effect': goal('fire')},
  {'name': 'Treasure F', 'base':'fire',  'effect': goal('fire')},
  {'name': 'Treasure F', 'base':'fire',  'effect': goal('fire')},
  {'name': 'Treasure W', 'base':'wind',  'effect': goal('wind')},
  {'name': 'Treasure W', 'base':'wind',  'effect': goal('wind')},
  {'name': 'Treasure W', 'base':'wind',  'effect': goal('wind')},
  {'name': 'Treasure W', 'base':'wind',  'effect': goal('wind')},
  {'name': 'Treasure W', 'base':'wind',  'effect': goal('wind')},
  {'name': 'Treasure M', 'base':'metal', 'effect': goal('metal')},
  {'name': 'Treasure M', 'base':'metal', 'effect': goal('metal')},
  {'name': 'Treasure M', 'base':'metal', 'effect': goal('metal')},
  {'name': 'Treasure M', 'base':'metal', 'effect': goal('metal')},
  {'name': 'Treasure M', 'base':'metal', 'effect': goal('metal')},
  {'name': 'Sandbags',   'base':'sandbag', 'effect': sandbag()},
  {'name': 'Sandbags',   'base':'sandbag', 'effect': sandbag()},
  {'name': 'Water Rise', 'base':'flood', 'effect': flood()},
  {'name': 'Water Rise', 'base':'flood', 'effect': flood()},
  {'name': 'Water Rise', 'base':'flood', 'effect': flood()},
]

"""
this is the basic structure of the game board
board = {
 'setup': 'standard',
 'active':0,
 'flood': [[],[]],
 'treasure': [[],[]],
 'tiles': [
   {'name': 'Helicopter Landing','state':0, 'base':'heliport'}, 
   {'name': 'Tresure W zone 2','state':1, 'base':'wind2' },
   {'name': 'Sunken','state':2, 'base':'water' } ],
 'players': [
   { 'userID':0,'nick':'anonymous','hand':[] },
   { 'userID':0,'nick':'anonymous','hand':[] },
   { 'userID':0,'nick':'anonymous','hand':[] },
   { 'userID':0,'nick':'anonymous','hand':[] },
   { 'userID':0,'nick':'anonymous','hand':[] },
   { 'userID':0,'nick':'anonymous','hand':[] }],
}
"""

main = """
<div style="font-size:15pt; font-weight:350; color: red;">
hello {0}
</div>
"""

class ForbidPlayer(ndb.Model):
    userID = ndb.StringProperty()
    board  = ndb.StringProperty()

def generateBoard(type):
  t = tiles[:]
  random.shuffle(t)
  fl = t[:]
  random.shuffle(fl)
  tr = treasure[:]
  random.shuffle(tr)
  board = {
 'setup': type,
 'active': 1,
 'tiles': t,
 'players': [],
 'flood':[fl[6:],fl[0:5]],
 'treasure': [tr,[]],
  }
  
  for x in board['flood'][1]:
    for s in t:
      if x['base'] == s['base']:
        s['state'] += 1
  return board

class gameHandler ( webapp2.RequestHandler ):
  def get (self):
    content = 'application/json'
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url (self.request.uri))
      return

    get_user_boards = ForbidPlayer.query(ForbidPlayer.userID == user.user_id())
    brd_ids = []
    brd = None
    for user_board in get_user_boards:
        brd_ids.append(user_board.board)
    brds = memcache.get_multi(brd_ids)
    resp = self.response
    resp.headers ['Content-Type'] = content
    if len(brds) < 1:
        brd = generateBoard('standard')
        newbid = user.user_id() + ':1'
        brd['bid'] = newbid
        memcache.add(newbid, brd)
        to_store = ForbidPlayer()
        to_store.userID = user.user_id()
        to_store.board  = newbid
        to_store.put()
    else:
        brd = brds.values()[0]
    resp.write (json.dumps(brd))

#application = webapp2.WSGIApplication ([
#    ('/', mainHandler),
#    ('/rest/v1/getCurrentBoard', gameHandler),
#], debug=True)
