import urllib, logging
from google.appengine.api import users
from google.appengine.ext import ndb
from feed import *
from models import *

class AdminHandler(AdminBaseHandler):

    def get(self):
        user = users.get_current_user()
        current = ndb.Key(CurrentFeed, 'current').get()
        if not current:
            current = CurrentFeed(id='current')
        if self.request.get('kill') == 'True':
            current.hangout = None
            current.youtube = None
            current.put()
        template_values = {
            'hangout_exists': current.hangout != None and current.youtube != None,
            'hangout_link': current.hangout.get().url if current.hangout else '',
            'youtube_link': current.youtube.get().video if current.youtube else 'dQw4w9WgXcQ'
        }
        self.render_template('admin-home.html', template_values)

class AdminHistory(AdminBaseHandler):

    def get(self):
        user = users.get_current_user()
        query = Youtube.query().order(-Youtube.time)
        youtube_list = query.fetch()
        template_values = {
            'youtube_list': youtube_list
        }
        self.render_template('admin-history.html', template_values)

class AdminSettings(AdminBaseHandler):

    def get(self):
        self._serve_page()

    def post(self):
        email_recipients = self.request.get("email-recipients")
        logging.info(email_recipients)
        settings = ndb.Key(Settings, 'settings').get()
        if not settings:
            settings = Settings(id='settings')
        settings.email_recipients = email_recipients.split("\r\n")
        settings.put()
        self._serve_page()

    def _serve_page(self):
        settings = ndb.Key(Settings, 'settings').get()
        if not settings:
            settings = {}
        template_values = {
            'settings': settings
        }
        self.render_template('admin-settings.html', template_values)

application = webapp2.WSGIApplication([
    ('/admin/history', AdminHistory),
    ('/admin/settings', AdminSettings),
    ('/admin.*', AdminHandler)
], debug=True)
