import os, urllib
from google.appengine.api import users
from feed import *
from models import *

class MainHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()
        if users.is_current_user_admin():
            self.redirect("/admin")
        current = ndb.Key(CurrentFeed, 'current').get() 
        if not current:
            current = CurrentFeed(id='current')
        template_values = {
            'hangout_exists': current.hangout != None and current.youtube != None,
            'hangout_link': current.hangout.get().url if current.hangout else '',
            'youtube_link': current.youtube.get().video if current.youtube else 'dQw4w9WgXcQ'
        }
        self.render_template('index.html', template_values)

application = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
