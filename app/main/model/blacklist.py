from .. import db
import datetime

class BlacklistToken(db.Document):
    token = db.StringField(required=True, unique=True)
    blacklisted_on = db.DateTimeField(required=True)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        try:
            res = BlacklistToken.objects.get(token=auth_token).first()
            if res:
                return True
            else:
                return False
        except:
            return False