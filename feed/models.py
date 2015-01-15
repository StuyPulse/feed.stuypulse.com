from google.appengine.ext import ndb

class Hangout(ndb.Model):
    url = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class Youtube(ndb.Model):
    video = ndb.StringProperty()
    title = ndb.StringProperty(default='')
    time = ndb.DateTimeProperty(auto_now_add=True)

class CurrentFeed(ndb.Model):
    hangout = ndb.KeyProperty(default=None)
    youtube = ndb.KeyProperty(default=None)
    update = ndb.DateTimeProperty(auto_now=True)
