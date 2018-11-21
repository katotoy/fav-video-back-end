from . import db, now
from pony.orm import select, count
import pony.orm as pny
from datetime import date


class VideoLikes(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    member_id = pny.Required(int)
    video_id = pny.Required(int)
    last_update = pny.Optional(date)

    @staticmethod
    def getUserLikeCount(member_id):

        try:
            rows = db.select('''select videos.id, videos.member_id, count(videolikes.id)
            from videos, videolikes where videos.id = videolikes.video_id and videos.member_id = {}
            group by videos.id, videos.member_id
            '''.format(member_id))

        except Exception as e:
            print('Exception Occued. class VideoLikes, method getUserLikeCount.', e)
            raise e

        return rows

    @staticmethod
    def didMemberLikedTheVideo(video_id, member_id):
        try:

            #check if the member already like the video, then delete the like

            likeCount = count(v for v in VideoLikes if v.video_id == video_id and v.member_id == member_id)

        except Exception as e:
            print('Exception Occued. class VideoLikes, method didmemberLikedTheVideo.', e)
            raise e

        # if likecount is greater than zero, the member liked the video
        return likeCount > 0

    @staticmethod
    def getLikeCount(video_id):
        try:
            return count(v for v in VideoLikes if v.video_id == video_id)
        except Exception as e:
            print('Exception Occurred. class VideoLikes, method getLikeCount.', e)
            raise e

    @staticmethod
    def save_like(video_id, member_id):

        try:

            # check if the member already like the video, then delete the like
            liked = select(v for v in VideoLikes if v.video_id == video_id and v.member_id == member_id)

            # print(liked.first().id)
            # no existing record found, add record for a like by a member
            if liked.first() is None:
                like = VideoLikes(video_id=video_id, member_id=member_id, last_update=now)
            # else delete/unlike
            else:
                like = VideoLikes[liked.first().id].delete()

            db.commit()

        except Exception as e:
            print('Exception Occued. class VideoLikes, method save_like.', e)
            raise e

        # return false (unliked) - true (liked)
        return liked is None

