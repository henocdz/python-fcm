import json
import requests

from .errors import AuthenticationError, FCMBadRequest, FCMServerError


class FCM(object):
    CONTENT_TYPE = 'application/json'
    FCM_ENDPOINT = 'https://fcm.googleapis.com/fcm/send'

    # FCM only allows up to 1000 registration ids per bulk message
    FCM_MAX_RECIPIENTS = 1000

    def __init__(self, api_key=None):
        if api_key is None:
            raise AuthenticationError("Please provide an API Key")
        else:
            self._FCM_API_KEY = api_key

    def send_request(self, payload):
        response = requests.post(self.FCM_ENDPOINT, data=payload, headers={
                                 "Content-Type": self.CONTENT_TYPE,
                                 "Authorization": "key=" + self._FCM_API_KEY,})
        return self.parse_response(response)

    def chunk_registration_ids(self, registration_ids):
        """Returns generator of lists that are consecutive subsets of
        the `registration_ids` list.
        """
        for i in range(0, len(registration_ids), self.FCM_MAX_RECIPIENTS):
            yield registration_ids[i:i + self.FCM_MAX_RECIPIENTS]

    def parse_response(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthenticationError("There was an error authenticating the sender account")
        elif response.status_code == 400:
            raise FCMBadRequest(response.content)
        else:
            raise FCMServerError("FCM server is temporarily unavailable")

    def create_payload(self, registration_ids=None, topic=None, condition=None,
                       notification=None, data=None, **kwargs):
        """Helper that accepts one of (`to`, `registration_ids`, `topic`,
        `condition`), and returns JSON payload to be passed with request.
        """
        payload = {}
        if registration_ids:
            if len(registration_ids) == 1:
                payload['to'] = registration_ids[0]
            else:
                payload['registration_ids'] = registration_ids
        elif topic:
            payload['to'] = '/topics/{}/'.format(topic)
        elif condition:
            payload['condition'] = condition

        if notification is not None:
            payload['notification'] = dict(notification)
        if data is not None:
            payload['data'] = dict(data)

        payload.update(kwargs)
        return json.dumps(payload)

    def send_messages(self, registration_ids=None, **kwargs):
        """Sends messages to recipients specified by `registration_ids`,
        `topic`, or `condition`.

        Invokes `create_payload` to create request bodies.
        """
        if isinstance(registration_ids, str):
            registration_ids = [registration_ids]

        responses = []
        if registration_ids and len(registration_ids) > 1:
            for chunk in self.chunk_registration_ids(registration_ids):
                payload = self.create_payload(registration_ids=registration_ids, **kwargs)
                responses.append(self.send_request(payload))
        else:
            payload = self.create_payload(registration_ids=registration_ids, **kwargs)
            responses.append(self.send_request(payload))
        return responses
