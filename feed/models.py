from google.appengine.ext import ndb

class HangoutUrl(ndb.Model):
    content = ndb.StringProperty()
    time = ndb.DateTimeProperty()
