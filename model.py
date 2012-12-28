from google.appengine.ext import db

class Msg(db.Model):
    ToUserName = db.StringProperty()

class TopTenTopic(db.Model):
    url = db.StringProperty()
    title = db.StringProperty()
    authorPic = db.StringProperty()
    rank = db.IntegerProperty()

class User(db.Model):
    wechatId = db.StringProperty()
    msgCount = db.IntegerProperty(default = 0)
    createDate = db.DateTimeProperty(auto_now_add = True)
    role = db.IntegerProperty(default = 0)

class MessageLog(db.Model):
    fromUser = db.ReferenceProperty(User)
    req = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)

class Pattern(db.Model):
    input = db.StringProperty()
    output = db.TextProperty()

class Weather(db.Model):
    day = db.IntegerProperty()
    temp = db.StringProperty()
    desc = db.StringProperty()
    wind = db.StringProperty(default = '')
    updateTime = db.DateTimeProperty(auto_now = True)

class Alias(db.Model):
    origin = db.StringProperty()
    result = db.StringProperty()

class ClassRoom(db.Model):
    name = db.StringProperty()
    shortcut = db.StringProperty()