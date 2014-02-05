from feed import JINJA_ENVIRONMENT, HangoutUrl
import webapp2, urllib
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Set the cross origin resource sharing header to allow AJAX
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")

        user = users.get_current_user()
        if users.is_current_user_admin():
            self.redirect("/admin")
        template_values = {
            'hangout_exists': not HangoutUrl.get_by_id(694) is None,
            'hangout_link': '' if HangoutUrl.get_by_id(694) is None else HangoutUrl.get_by_id(694).content
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
