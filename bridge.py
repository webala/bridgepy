import requests, os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

#load environment variables
load_dotenv()

class Bridge():

    @property
    def auth_url(_):
        return "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    def __init__(self, consumer_key, consumer_secret, business_shortcode, passkey) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_shortcode = business_shortcode
        self.passkey = passkey
   
    def authenticate(self):
        '''
        Makes a request to the auth endndpoint and raise an exception if an error response is returned
        On success, status 200, get the access token and return it
        '''
        try:
        
         response = requests.get(self.auth_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
         response.raise_for_status()

         json_res = response.json()
         access_token = json_res.get('access_token')

         return access_token
        
        except requests.exceptions.RequestException as e:
         print('Authenticate error: ', e)


    def _generate_password(self):
      #  data_to_encode = str(self.business_shortcode + self.passkey + timestamp)
      pass
        

bridge = Bridge(
   consumer_key=os.getenv('CONSUMER_KEY'),
   consumer_secret=os.getenv('CONSUMER_SECRET'),
   business_shortcode=os.getenv('SHORT_CODE'),
   passkey=os.getenv('PASSKEY')
)

print(bridge.authenticate())