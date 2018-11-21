from . import db, now
import pony.orm as pny
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


class Members(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    email = pny.Required(str)
    call_sign = pny.Required(str)
    password = pny.Required(str)
    join_date = pny.Optional(datetime.date)
    isadmin = pny.Optional(bool)

    @staticmethod
    def get_member(member_id):
        try:
            return Members[member_id]
        except Exception as e:
            print('Exception occurred. class members, method get_member', e)
            raise e

    @staticmethod
    def save_member(email, call_sign, password, id=None):

        try:

            # Saving a new member record
            if id is None:
                rec = Members(email=email, call_sign=call_sign,
                              password=sha256.hash(password), join_date=now, isadmin=False)

            else:
                rec = Members[id];
                rec.set(call_sign=call_sign, password=sha256.hash(password))

            db.commit()

            return rec

        except Exception as e:
            print('Exception occurred. class Members, method save_member.', e)
            raise e
