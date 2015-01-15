import logging
from datetime import datetime
from feed import *
from models import *

class HangoutHandler(BaseHandler):

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed(id='current')
        current.update = datetime.now()

        hangout_url = self.request.get('hangoutUrl')
        hangout = None
        if hangout_url != '':
            logging.info("Hangout Url: %s" % hangout_url)
            hangout = Hangout()
            hangout.url = hangout_url
            hangout.put()
            current.hangout = hangout.key

        youtube_id = self.request.get('youtubeId')
        youtube = None
        if youtube_id != '':
            logging.info("Youtube Id: %s" % youtube_id)
            youtube = Youtube()
            youtube.video = youtube_id
            youtube.put()
            current.youtube = youtube.key

        current.put()

class HangoutKiller(BaseHandler):

    def get(self):
        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed()

        if (datetime.now() - current.update).seconds > 300:
            current.hangout = None
            current.youtube = None
            current.put()

application = webapp2.WSGIApplication([
    ('/hangout_kill', HangoutKiller),
    ('/hangout.*', HangoutHandler)
], debug=True)
