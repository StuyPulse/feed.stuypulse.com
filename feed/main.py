from feed import JINJA_ENVIRONMENT
import webapp2, urllib
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Set the cross origin resource sharing header to allow AJAX
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))

application = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
