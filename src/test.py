import unittest, os
import bridge.bridge as daraja


class TestBridge(unittest.TestCase):
    def test_authenticate_success(self):
        """
        Tests the authentication function for correct response
        """
        bridge = daraja.Bridge(
            consumer_key=os.getenv("CONSUMER_KEY"),
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            business_shortcode=os.getenv("SHORT_CODE"),
            passkey=os.getenv("PASSKEY"),
            app_name="bridge",
            callback_url="https://callback.url.com",
        )
        auth = bridge.authenticate()
        self.assertIn("access_token", auth)

    def test_authenticate_fail(self):
        """
        Test for authentication function for auth failed due to wrong key
        """
        bridge = daraja.Bridge(
            consumer_key="",
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            business_shortcode=os.getenv("SHORT_CODE"),
            passkey=os.getenv("PASSKEY"),
            app_name="bridge",
            callback_url="https://callback.url.com",
        )
        auth = bridge.authenticate()
        self.assertIsNone(auth)

    def test_initiate_stk_success(self):
        '''
        Success case test for initiate stk push
        '''
        bridge = daraja.Bridge(
            consumer_key=os.getenv("CONSUMER_KEY"),
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            business_shortcode=os.getenv("SHORT_CODE"),
            passkey=os.getenv("PASSKEY"),
            app_name="bridge",
            callback_url="https://callback.url.com",
        )
        response = bridge.initialize_stk("254791055897", "Bridge first test")
        response_code = response.get("response_code")
        self.assertEqual(response_code, "0")

    def test_wrong_phone_number_response(self):
        bridge = daraja.Bridge(
            consumer_key=os.getenv("CONSUMER_KEY"),
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            business_shortcode=os.getenv("SHORT_CODE"),
            passkey=os.getenv("PASSKEY"),
            app_name="bridge",
            callback_url="https://callback.url.com",
        )
        response = bridge.initialize_stk("91055897", "Test wrong phone number response")
        print('wrong phone res: ', response)
      #   response_code = response.get("response_code")
      #   self.assertEqual(response_code, "0")


