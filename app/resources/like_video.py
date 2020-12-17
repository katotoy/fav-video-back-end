from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..entities import videolikes as vl
import json


class LikeVideo(Resource):

    @staticmethod
    def get(video_id):
        print('Checking if member liked the video')

        member_id = get_jwt_identity()

        try:
            did_member_liked = vl.VideoLikes.didMemberLikedTheVideo(video_id, member_id)
            response = {
                "member_id": member_id,
                "video_id": video_id,
                "message": "Checking if member liked the video",
                "did_member_liked": did_member_liked
            }
            http_code = 201

        except Exception as e:
            response = {
                "status": 400,
                "exception": e,
                "message": "Error occurred while checking if member liked the video: ()".format(video_id)
            }
            http_code = 400

        return response, http_code

    @staticmethod
    @jwt_required
    def post(video_id):
        print('Liking\\Unliking A Video', video_id)

        member_id = get_jwt_identity()

        try:
            user_liked = vl.VideoLikes.save_like(video_id, member_id)

            return {
                "status": 200,
                "member_id": member_id,
                "video_id": video_id,
                "message": "toggling if member liked a video",
                "did_member_liked": user_liked
            }, 201

        except Exception as e:
            print(e)
            return {
                "status": 400,
                "message": "toggling if member liked a video",
                "did_member_liked": "an error occurred / unable to determine"
            }, 400


class VideoLikeCount(Resource):
    @staticmethod
    def get(video_id):
        print('Getting Like Count of Video: ', video_id)

        try:
            like_count = vl.VideoLikes.getLikeCount(video_id)
            print(like_count)
            response = {
                "videoID": video_id,
                "message": "Number of Likes retrieved.",
                "like_count": like_count
            }
            http_code = 201

        except Exception as e:
            print(e)
            response = {
                "message": "Error occurred while trying to get like count of video ()".format(video_id)
            }
            http_code = 400

        return response, http_code


class UserVideosLikeCount(Resource):

    @staticmethod
    def get(member_id):
        print('Getting Like Count of Videos by : ', member_id)

        try:
            user_like_count = vl.VideoLikes.getUserLikeCount(member_id)

            user_count_like_result = []

            for row in user_like_count:
                item = {
                    "videoID":row[0],
                    "memberID": row[1],
                    "likeCount": row[2]
                }
                user_count_like_result.append(item)

            return json.dumps(user_count_like_result), 200

        except Exception as e:
            print('Method get of UserVideosLikeCount Exception', e)
            response = {
                "message": "Error occurred while trying to get the "
                           "number of likes of video/s by member {}".format(member_id)
            }
            return response, 404

