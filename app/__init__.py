from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from pony.flask import Pony

from .resources import user, video, like_video
from .entities import setup_db

app = Flask(__name__, static_url_path='')
app.secret_key = 'ThEc0de15'
api = Api(app)
jwt = JWTManager(app)
Pony(app)

@app.route('/')
def serve_page():
    return app.send_static_file('index.html')


@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'authorization, content-type'
    return response


def add_resources():
    api.add_resource(user.User, '/user')
    api.add_resource(user.UserLogin, '/login')
    api.add_resource(video.Videos, '/videos/<int:video_id>', '/videos')
    api.add_resource(video.AllVideos, '/gallery')
    api.add_resource(like_video.LikeVideo, '/like-videos/<int:video_id>')
    api.add_resource(like_video.VideoLikeCount, '/video-like-count/<int:video_id>')
    api.add_resource(like_video.UserVideosLikeCount, '/user-videos-like-count/<int:member_id>')
    api.add_resource(video.UserVideos, '/user-videos')


add_resources()
setup_db(True) # set to True if going live