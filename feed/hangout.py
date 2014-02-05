import webapp2
from feed import HangoutUrl

class HangoutHandler(webapp2.RequestHandler):

    def post(self):
        hangout = self.request.get('hangoutUrl')
        hangoutUrl = HangoutUrl(id=1)
        hangoutUrl.content = url
        hangoutUrl.put()
        youtube = self.request.get('youtubeId')
        youtubeUrl = HangoutUrl(id=2)
        youtubeUrl.content = youtube
        youtubeUrl.put()
