import requests, os, base64, json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime

# load environment variables
load_dotenv()


class Bridge:
    @property
    def auth_url(_):
        return "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    @property
    def stk_url(_):
        return "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        business_shortcode,
        passkey,
        app_name,
        callback_url,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_shortcode = business_shortcode
        self.passkey = passkey
        self.app_name = app_name
        self.callback_url = callback_url

    def authenticate(self):
        """
        Makes a request to the auth endndpoint and raise an exception if an error response is returned
        On success, status 200, get the access token and return it
        """
        try:
            response = requests.get(
                self.auth_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
            response.raise_for_status()

            json_res = response.json()
            # access_token = json_res.get("access_token")

            return json_res

        except requests.exceptions.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                print(
                    "Authenticate errored out with code",
                    e.response.status_code,
                    e.response,
                )
            else:
                print("An error occurred: ", e)

    def _generate_payload(self, phone_number, transaction_description, amount=1):
        """
        This function generates the payload that will be used in the initiate stk push request.
        """
        # Genetate a timeastamp in the format year, month, day, hour, minutes, seconds
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d%H%M%S")

        # Generate the password.
        # A base64 encoded string. (The base64 string is a combination of Shortcode+Passkey+Timestamp)
        data_to_encode = self.business_shortcode + self.passkey + timestamp
        password = base64.b64encode(data_to_encode.encode("utf-8")).decode("utf-8")

        return {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": self.app_name,
            "TransactionDesc": transaction_description,
        }

    def initialize_stk(self, phone_number, transaction_description):
        auth = self.authenticate()
        access_token = auth.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = self._generate_payload(phone_number, transaction_description)

        try:
            response = requests.post(self.stk_url, headers=headers, json=payload)
            json_res = json.loads(response.text)

            return {
                "merchant_request_id": json_res.get("MerchantRequestID"),
                "chechout_request_id": json_res.get("CheckoutRequestID"),
                "response_code": json_res.get("ResponseCode"),
                "response_description": json_res.get("ResponseDescription"),
                "customer_meaasge": json_res.get("CustomerMessage"),
            }

        except requests.exceptions.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                print(
                    "Initiate stk push errored out with code",
                    e.response.status_code,
                    e.response,
                )
            else:
                print("An error occurred: ", e)
            return None



