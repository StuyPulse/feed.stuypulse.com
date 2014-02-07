from feed import JINJA_ENVIRONMENT, HangoutUrl
import webapp2, urllib
from google.appengine.api import users
from google.appengine.ext import ndb

class AdminHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                if self.request.get('kill') != 'True':
                    ndb.Key(HangoutUrl, 1).delete()
                    ndb.Key(HangoutUrl, 2).delete()
                template_values = {
                    'user': user.nickname(),
                    'logout_url': users.create_logout_url('/'),
                    'hangout_exists': not HangoutUrl.get_by_id(1) is None,
                    'hangout_link': '' if HangoutUrl.get_by_id(1) is None else HangoutUrl.get_by_id(1).content,
                    'youtube_link': 'dQw4w9WgXcQ' if HangoutUrl.get_by_id(2) is None else HangoutUrl.get_by_id(2).content
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
