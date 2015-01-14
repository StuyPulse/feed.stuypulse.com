import os, urllib
from google.appengine.api import users
from google.appengine.ext import ndb
from feed import *
from models import *

class AdminHandler(AdminBaseHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            if self.request.get('kill') == 'True':
                ndb.Key(HangoutUrl, 1).delete()
                ndb.Key(HangoutUrl, 2).delete()
            template_values = {
                'hangout_exists': not HangoutUrl.get_by_id(1) is None,
                'hangout_link': '' if HangoutUrl.get_by_id(1) is None else HangoutUrl.get_by_id(1).content,
                'youtube_link': 'dQw4w9WgXcQ' if HangoutUrl.get_by_id(2) is None else HangoutUrl.get_by_id(2).content
            }
            self.render_template('admin.html', template_values)
        else:
            self.redirect('/')

application = webapp2.WSGIApplication([
    ('/admin.*', AdminHandler)
], debug=True)
