from feed import JINJA_ENVIRONMENT
import webapp2, urllib
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):

    def get(self):
        # Set the cross origin resource sharing header to allow AJAX
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.redirect("/admin")
            template_values = {
                'logout_url': users.create_logout_url("/")
            }
            template = JINJA_ENVIRONMENT.get_template('hangouts.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url("/"))

application = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
