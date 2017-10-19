from base64 import urlsafe_b64decode
import httplib2
from oauth2client import client


class TSKeyCloakConnector:
    __TOKEN_URI = ""
    __CLIENT_SECRET = ""
    __REVOKE_URI = ""
    __CLIENT_ID = ""
    at = None
    at_expiry = None
    refresh_token = None

    def __init__(self, client_id, client_secret, token_uri, revoke_uri, refresh_token):
        self.__CLIENT_ID = client_id
        self.__CLIENT_SECRET = client_secret
        self.__TOKEN_URI = token_uri
        self.__REVOKE_URI = revoke_uri
        self.refresh_token = refresh_token

    def access_token(self):
        cred = client.OAuth2Credentials(self.at, self.__CLIENT_ID, self.__CLIENT_SECRET, self.refresh_token(),
                                        self.at_expiry, self.__TOKEN_URI, None, revoke_uri=self.__REVOKE_URI)
        print(cred.token_expiry)
        if not cred.access_token or cred.access_token_expired:
            # todo: remove
            cred.refresh(httplib2.Http(disable_ssl_certificate_validation=True))
            self.at = cred.access_token
            self.at_expiry = cred.token_expiry
            print("token expired and refreshed")
        self.print_decoded_token(cred.access_token)
        return cred.access_token

    def logout(self):
        cred = client.OAuth2Credentials(self.at, self.__CLIENT_ID, self.__CLIENT_SECRET, self.refresh_token(),
                                        self.at_expiry, self.__TOKEN_URI, None, revoke_uri=self.__REVOKE_URI)
        cred.revoke()

    @staticmethod
    def print_decoded_token(token):
        token = token.split(".")[1]
        missing_padding = len(token) % 4
        if missing_padding != 0:
            token += b'=' * (4 - missing_padding)
        print(urlsafe_b64decode(token))
