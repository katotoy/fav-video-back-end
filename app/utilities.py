from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt)


class TokenCreator:
    def __init__(self, id):
        self._access_token = create_access_token(identity=id, fresh=True, expires_delta=False)
        self._refresh_token = create_refresh_token(identity=id, expires_delta=False)

    def getAccessToken(self):
        return self._access_token

    def getRefreshToken(self):
        return self._refresh_token

