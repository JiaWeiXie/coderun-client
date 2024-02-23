import os
from requests import Session


BASE_URL = os.getenv("JUDGE0_URL", "")


class Judge0Client:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = Session()

    def get_languages(self):
        url = self.base_url + "/languages"
        response = self.session.get(url)
        return response.json()

    def get_language(self, language_id):
        url = self.base_url + "/languages/{}".format(language_id)
        response = self.session.get(url)
        return response.json()

    def get_submission(self, submission_id):
        url = self.base_url + "/submissions/{}".format(submission_id)
        response = self.session.get(url)
        return response.json()

    def create_submission(
        self,
        source_code,
        language_id,
        stdin=None,
        expected_output=None,
    ):
        url = self.base_url + "/submissions/?base64_encoded=false&wait=false"
        data = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": stdin,
            "expected_output": expected_output,
        }
        response = self.session.post(url, data=data)
        return response.json()

    def create_batch_submissions(self, data):
        url = self.base_url + "/submissions/batch?base64_encoded=false"
        response = self.session.post(url, json={"submissions": data})
        return response.json()

    def get_batch_submissions(self, tokens: str):
        url = self.base_url + "/submissions/batch"
        response = self.session.get(
            url,
            params={"tokens": tokens, "base64_encoded": "false"},
        )
        return response.json()
