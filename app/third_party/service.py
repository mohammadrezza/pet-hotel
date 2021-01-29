from typing import List, Dict
import requests


class Mailer:
    def __init__(self):
        self.sib_base_url = None
        self.sib_api_key = None

    def init_app(self, app):
        self.sib_base_url = app.config.get("SIB_BASE_URL", None)
        self.sib_api_key = app.config.get("SIB_API_KEY", None)

    def send_mail(self, subject: str, text: str, to: List[Dict]):
        try:
            response = requests.post(self.sib_base_url, headers={
                'api-key': self.sib_api_key
            }, json={
                "sender": {
                    "name": "sender name",
                    "email": "seder email"
                },
                "to": to,
                "subject": subject,
                "htmlContent": f"<html><head></head><body><p>Sign up to pet hotel now !</p>{text}</p></body></html>"
            })
            return True if response.status_code == 201 else False
        except Exception as e:
            print(e)
            return False
