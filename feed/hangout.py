import webapp2
from feed import HangoutUrl

class HangoutHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        hangout = self.request.get('hangoutUrl')
        hangoutUrl = HangoutUrl(id=1)
        hangoutUrl.content = url
        hangoutUrl.put()
        youtube = self.request.get('youtubeId')
        youtubeUrl = HangoutUrl(id=2)
        youtubeUrl.content = youtube
        youtubeUrl.put()

application = webapp2.WSGIApplication([
    ('/hangout', HangoutHandler)
], debug=True)
