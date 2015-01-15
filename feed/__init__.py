import os, webapp2, jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from jinja_functions import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])
JINJA_ENVIRONMENT.filters.update({
    'datetimeformat': jinja_functions.datetimeformat
})

class BaseHandler(webapp2.RequestHandler):

    def render_template(self, template_filename, template_values={}):
        template_values['page_url'] = self.request.url
        template = JINJA_ENVIRONMENT.get_template(template_filename)
        self.response.out.write(template.render(template_values))

class AdminBaseHandler(webapp2.RequestHandler):

    def render_template(self, template_filename, template_values={}):
        template_values.update({
            'page_url': self.request.url,
            'user_nickname': users.get_current_user().nickname(),
            'logout_url': users.create_logout_url('/')
        })
        template = JINJA_ENVIRONMENT.get_template(template_filename)
        self.response.out.write(template.render(template_values))
