import webapp2
from feed import HangoutUrl

class HangoutHandler(webapp2.RequestHandler):

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        hangout = self.request.get('hangoutUrl')
        if hangout != '':
            hangoutUrl = HangoutUrl(id=1)
            hangoutUrl.content = hangout
            hangoutUrl.put()
        youtube = self.request.get('youtubeId')
        if youtube != '':
            youtubeUrl = HangoutUrl(id=2)
            youtubeUrl.content = youtube
            youtubeUrl.put()

application = webapp2.WSGIApplication([
    ('/hangout', HangoutHandler)
], debug=True)
