import webapp2
from feed import HangoutUrl
from datetime import datetime
from google.appengine.api import mail

class HangoutHandler(webapp2.RequestHandler):

    def post(self):
        # Set the cross origin resource sharing header to allow AJAX
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        if self.request.headers['Referer'].find("googleusercontent.com") != -1:
            hangout = self.request.get('hangoutUrl')
            if hangout != '':
                hangoutUrl = HangoutUrl(id=1, content=hangout, not_sent=True, time=datetime.now())
                hangoutUrl.put()
            youtube = self.request.get('youtubeId')
            if youtube != '':
                youtubeUrl = HangoutUrl(id=2, content=youtube, not_sent=True)
                youtubeUrl.put()
            hangoutUrl = HangoutUrl.get_by_id(1)
            hangoutUrl.time = datetime.now()
            if hangoutUrl.not_sent == True and HangoutUrl.get_by_id(2).not_sent == True:
                mail.send_mail(sender="Stuypulse on Air <ntw3450@gmail.com>",
                               to="stuy694@yahoogroups.com",
                               subject="A Virtual Lab Feed has been started!",
                               body = "Hey all, this is an automated message informing you that a Google Hangouts for the lab is live at https://feed-stuypulse.appspot.com!",
                               html="""
<h1>Hey all!</h1>
<p>
    This is an automated message informing you that a Google Hangouts for the lab has been started!
    <br><br>
    You can <b>join</b> the hangout here: <a href="%s">%s</a>
    <br>
    Or, you can <b>watch</b> the youtube livestream here: <a href="https://feed-stuypulse.appspot.com">https://feed-stuypulse.appspot.com</a>
</p>
""" % (hangoutUrl.content, hangoutUrl.content))
                hangoutUrl.not_sent = False
                youtube_sent = HangoutUrl.get_by_id(2)
                youtube_sent.not_sent = False
                youtube_sent.put()
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
    ('/hangout_kill', HangoutKiller),
    ('/hangout', HangoutHandler)
], debug=True)
