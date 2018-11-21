from . import db, now
from pony.orm import select, desc
import pony.orm as pny
import datetime


class Videos(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    url = pny.Required(str)
    title = pny.Required(str)
    description = pny.Required(str)
    date_posted = pny.Optional(datetime.date)
    member_id = pny.Optional(int)
    last_update = pny.Optional(datetime.datetime)

    @staticmethod
    def delete_video(video_id):
        try:
            rec_delete = Videos[video_id]

            if rec_delete is not None:
                rec_delete.delete()

            return True

        except Exception as e:
            print('Exception occurred. class Videos, method delete_video', e)
            raise e

    @staticmethod
    def getUserVideos(member_id):
        try:
            user_videos = select(v for v in Videos if v.member_id == member_id) \
                .order_by(desc(Videos.last_update), desc(Videos.id))

        except Exception as e:
            print('Exception occurred. class Videos, method getUserVideos.', e)
            raise e

        return user_videos

    @staticmethod
    def getAllVideos():
        try:
            videos = select(v for v in Videos)
        except Exception as e:
            print('Exception occurred. class Videos, method getAllVideos.', e)
            raise e

        return videos

    @staticmethod
    def save_video(url, title, description='', member_id=0, id=0):
        try:
            if id == 0:
                record = Videos(url=url, title=title,
                                description=description, member_id=member_id, date_posted=now, last_update=now)
            # Save Edit
            else:
                record = Videos[id]
                record.set(url=url, title=title, description=description, last_update=now)

            db.commit()
        except Exception as e:
            print('Exception Occued. class Videos, method save_video.', e)
            raise e

        return record

