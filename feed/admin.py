import os, urllib
from google.appengine.api import users
from google.appengine.ext import ndb
from feed import *
from models import *

class AdminHandler(AdminBaseHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            current = ndb.Key(CurrentFeed, 'current').get()
            if not current:
                current = CurrentFeed(id='current')
            if self.request.get('kill') == 'True':
                current.hangout = None
                current.youtube = None
            template_values = {
                'hangout_exists': current.hangout != None and current.youtube != None,
                'hangout_link': current.hangout.get().url if current.hangout else '',
                'youtube_link': current.youtube.get().video if current.youtube else 'dQw4w9WgXcQ'
            }
            self.render_template('admin.html', template_values)
        else:
            self.redirect('/')

application = webapp2.WSGIApplication([
    ('/admin.*', AdminHandler)
], debug=True)
