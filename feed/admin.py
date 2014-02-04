from feed import JINJA_ENVIRONMENT
import webapp2, urllib
from google.appengine.api import users
from google.appengine.ext import ndb

class HangoutUrl(ndb.Model):
    content = ndb.StringProperty()

class AdminHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                template_values = {
                    'user': user.nickname(),
                    'logout_url': users.create_logout_url('/'),
                    'hangout_exists': not HangoutUrl.get_by_id(694) is None,
                    'hangout_link': '' if HangoutUrl.get_by_id(694) is None else HangoutUrl.get_by_id(694).content
                }
                template = JINJA_ENVIRONMENT.get_template('admin.html')
                self.response.write(template.render(template_values))
            else:
                self.redirect('/')
        else:
            login_url = users.create_login_url('/admin')
            self.redirect(login_url)

    def post(self):
        isRequestToRemove = (self.request.get('remove_hangout_url') != '')
        if isRequestToRemove:
            ndb.Key(HangoutUrl, 694).delete() 
            self.response.write("URL removed.")
        else:
            url = self.request.get('show_hangout_url')
            hangoutUrl = HangoutUrl(id=694)
            hangoutUrl.content = url
            hangoutUrl.put()
            self.response.write("Displaying hangout URL: \n" + url)

application = webapp2.WSGIApplication([
    ('/admin.*', AdminHandler)
], debug=True)
