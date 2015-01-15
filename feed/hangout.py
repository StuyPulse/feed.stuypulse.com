from datetime import datetime
from feed import *
from models import *

class HangoutHandler(BaseHandler):

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")

        hangout_url = self.request.get('hangoutUrl')
        hangout = None
        if hangout_url != '':
            hangout = Hangout()
            hangout.url = hangout_url
            hangout.put()

        youtube_id = self.request.get('youtubeId')
        youtube = None
        if youtube_id != '':
            youtube = Youtube()
            youtube.video = youtube_id
            youtube.put()

        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed(id='current')
        current.hangout = hangout.key
        current.youtube = youtube.key
        current.put()

class HangoutKiller(BaseHandler):

    def get(self):
        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed()

        if current.hangout:
            hangout = current.hangout.get()
            if hangout:
                if (datetime.now() - hangout.time).seconds > 300:
                    current.hangout = None
                    current.youtube = None
                    current.put()

application = webapp2.WSGIApplication([
    ('/hangout_kill', HangoutKiller),
    ('/hangout.*', HangoutHandler)
], debug=True)
