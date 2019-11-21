import requests, json, os
global session
import keyring

class AllegroRestApi():

    #TODO MAKE ALL SECRETS USING KEYRING
    def __init__(self):
        self.DEFAULT_OAUTH_URL = 'https://allegro.pl/auth/oauth'
        self.DEFAULT_REDIRECT_URI = 'http://localhost:8000'
        self.DEFAULT_API_URL = 'https://api.allegro.pl'
        self.api_key =  keyring.get_password('api_key', 'czemutaktanio')
        self.client_id = keyring.get_password('client_id', 'czemutaktanio')
        self.client_secret = keyring.get_password('client_secret', 'czemutaktanio')
        self.access_token = keyring.get_password('access_token', 'czemutaktanio')
        self.refresh_token = keyring.get_password('refresh_token', 'czemutaktanio')
        self.refresh_token_response = ''

        self.do_refresh_token()
        self.get_new_acess_token()
        self.get_new_refresh_token()


    def do_refresh_token(self):
        token_url = self.DEFAULT_OAUTH_URL + '/token'

        access_token_data = {'grant_type': 'refresh_token',
                             'api-key': self.api_key,
                             'refresh_token': self.refresh_token,
                             'redirect_uri': self.DEFAULT_REDIRECT_URI}

        response = requests.post(url=token_url,
                                 auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret),
                                 data=access_token_data)

        self.refresh_token_response = json.loads(response.content.decode('utf-8'))

    def get_new_acess_token(self):
        self.access_token = self.refresh_token_response['access_token']
        keyring.set_password('access_token', 'czemutaktanio', '{}'.format(self.access_token))

    def get_new_refresh_token(self):
        self.refresh_token = self.refresh_token_response['refresh_token']
        keyring.set_password('refresh_token', 'czemutaktanio', '{}'.format(self.refresh_token))
