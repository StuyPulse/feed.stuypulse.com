from feed import JINJA_ENVIRONMENT
import webapp2, urllib
from google.appengine.api import users

class AdminHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                template_values = {
                    'user': user.nickname(),
                    'logout_url': users.create_logout_url('/'),
                }
                template = JINJA_ENVIRONMENT.get_template('admin.html')
                self.response.write(template.render(template_values))
            else:
                self.redirect('/')
        else:
            login_url = users.create_login_url('/admin')
            self.redirect(login_url)

application = webapp2.WSGIApplication([
    ('/admin.*', AdminHandler)
], debug=True)
