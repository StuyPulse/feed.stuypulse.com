import webapp2
from feed import HangoutUrl
from datetime import datetime
from google.appengine.ext import ndb

class HangoutHandler(webapp2.RequestHandler):

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        hangout = self.request.get('hangoutUrl')
        if hangout != '':
            hangoutUrl = HangoutUrl(id=1, content=hangout)
            hangoutUrl.put()
        youtube = self.request.get('youtubeId')
        if youtube != '':
            youtubeUrl = HangoutUrl(id=2, content=youtube)
            youtubeUrl.put()
        hangoutUrl = HangoutUrl.get_by_id(1)
        hangoutUrl.time = datetime.now()
        hangoutUrl.put()

class HangoutKiller(webapp2.RequestHandler):

    def get(self):
        hangout = HangoutUrl.get_by_id(1)
        youtube = HangoutUrl.get_by_id(2)
        diff = datetime.now() - hangout.time
        if diff.seconds > 240:
            ndb.Key(HangoutUrl, 1).delete()
            ndb.Key(HangoutUrl, 2).delete()

application = webapp2.WSGIApplication([
    ('/hangout', HangoutHandler),
    ('/hangout_kill', HangoutKiller)
], debug=True)
