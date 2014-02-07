import webapp2, datetime
from feed import HangoutUrl

class HangoutHandler(webapp2.RequestHandler):

    def get(self):
        hangout = HangoutUrl(id=1)
        youtube = HangoutUrl(id=2)
        diff = datetime.datetime.now() - hangoutUrl.time
        if diff.seconds > 240:
            hangout.delete()
            youtube.delete()

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        hangout = self.request.get('hangoutUrl')
        if hangout != '':
            hangoutUrl = HangoutUrl(id=1, content=hangout)
            hangoutUrl.put()
        youtube = self.request.get('youtubeId')
        if youtube != '':
            youtubeUrl = HangoutUrl(id=2, content=hangout)
            youtubeUrl.put()
        if self.request.get('time') != '':
            HangoutUrl(id=1, still_alive=True).put()

application = webapp2.WSGIApplication([
    ('/hangout', HangoutHandler)
], debug=True)
