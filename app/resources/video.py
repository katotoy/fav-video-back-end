from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from ..entities import videos as vid


class Videos(Resource):

    @staticmethod
    @jwt_required
    def delete(video_id):
        print('delete a video', video_id)

        try:
            if vid.Videos.delete_video(video_id):
                return {
                    "status": "200",
                    "action": "delete a video record",
                    "video_id": video_id
                }, 200

        except Exception as e:
            print('Error occurred while deleting a video with id {}'.format(video_id), e)
            return {
                "message": "An error occurred while trying to delete a video"
            }, 400

    @staticmethod
    def get(video_id):

        if video_id is None:
            print('Retrieve Video Details with ID', video_id)

        video = vid.Videos[video_id]

        if video is not None:
            return {
                "id": video.id,
                "url": video.url,
                "title": video.title,
                "description": video.description,
                "date_posted" : str(video.date_posted),
                "member_id": video.member_id
            }, 200

        return 'Requested Video Not Found', 400

    @jwt_required
    def post(self, video_id=0):

        if video_id == 0:
            print('Add New Video')
        else:
            print('Saving Changes for an existing video', video_id)

        member_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('url', help='This field cannot be blank', required=True)
        parser.add_argument('title', help='This field cannot be blank', required=True)
        parser.add_argument('description', help='This field cannot be blank')

        args = parser.parse_args()
        http_code = 0

        try:
            video = vid.Videos.save_video(args['url'], args['title'],
                                          args['description'], member_id, video_id)

            print(video)
            response = {
                "id": video.id,
            }
            http_code = 201

        except Exception as e:
            print(e)
            response = {
                "id": "Error while adding a new video",
            }
            http_code = 400

        return response, http_code


class UserVideos(Resource):

    @staticmethod
    @jwt_required
    def get():

        member_id = get_jwt_identity()
        print('Getting Videos of Member ID: ', member_id)

        try:
            user_videos = vid.Videos.getUserVideos(member_id)

            video_lists = []
            for video in user_videos:
                item = {
                    "id": video.id,
                    "url": video.url,
                    "title": video.title,
                    "description": video.description,
                    "date_posted": str(video.date_posted),
                    "member_id": video.member_id
                }

                video_lists.append(item)

            return json.dumps(video_lists), 200

        except Exception as e:
            print(e)
            response = {
                "message": "Error occured while getting shared videos by Member ID ()".format(member_id)
            }
            http_code = 400
            return response, http_code


class AllVideos(Resource):

    @staticmethod
    def get():
        videos = vid.Videos.getAllVideos()

        try:
            video_list = []
            for video in videos:

                item = {
                    "id": video.id,
                    "url": video.url,
                    "title": video.title,
                    "description": video.description,
                    "date_posted": str(video.date_posted),
                    "member_id":video.member_id
                }

                video_list.append(item)

            return json.dumps(video_list), 200

        except Exception as e:
            print('An Exception occurred: ', e)
            return 'An Error occurred while retrieving list of videos', 400



