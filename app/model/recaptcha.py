import os, requests, json


def google_recaptchaV2(client_recaptcha='', test=False):
    google_secret_key = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    google_test_secret_key = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    google_test_client_key = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                    data = {'secret': google_secret_key if test is False else google_test_secret_key,
                            'response': client_recaptcha if test is False else google_test_client_key},
                    timeout=10)
    google_response = json.loads(r.text)    # CONVERTS GOOGLE'S RESPONSE

    return google_response