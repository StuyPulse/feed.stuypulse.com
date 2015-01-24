import logging
from datetime import datetime
from google.appengine.api import mail
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
        if hangout_url != '' and not current.hangout:
            logging.info("Hangout Url: %s" % hangout_url)
            hangout = Hangout()
            hangout.url = hangout_url
            hangout.put()
            current.hangout = hangout.key

        youtube_id = self.request.get('youtubeId')
        youtube = None
        if youtube_id != '' and not current.youtube:
            logging.info("Youtube Id: %s" % youtube_id)
            youtube = Youtube()
            youtube.video = youtube_id
            youtube.put()
            current.youtube = youtube.key

        if current.hangout and current.youtube and not current.email_sent:
            settings = ndb.Key(Settings, 'settings').get()
            mail.send_mail(sender="Stuypulse on Air <dqiu55@gmail.com>",
                           to="%s" % (', '.join(settings.email_recipients)),
                           subject="A Virtual Lab Feed has been started!",
                           body="Hey all, this is an automated message informing you that a Google Hangouts for the lab is live at https://feed-stuypulse.appspot.com!",
                           html="""
<h1>Hello!</h1>
<p>This is an automated message informing you that a Google Hangouts for the lab has been started!</p>
<p>You can <b>join</b> the hangout here: <a href="%s">%s</a></p>
<p>Or, you can <b>watch</b> the youtube livestream here: <a href="https://feed-stuypulse.appspot.com">https://feed-stuypulse.appspot.com</a></p>
""" % (current.hangout.get().url, current.hangout.get().url))
            current.email_sent = True

        current.put()

class HangoutKiller(BaseHandler):

    def get(self):
        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed()

        if (datetime.now() - current.update).seconds > 300:
            current.hangout = None
            current.youtube = None
            current.email_sent = False
            current.put()

application = webapp2.WSGIApplication([
    ('/hangout_kill', HangoutKiller),
    ('/hangout.*', HangoutHandler)
], debug=True)
