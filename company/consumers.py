import json

from channels.generic.websocket import WebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope["user"])
        if self.scope["user"].is_authenticated:
            self.accept()
        else:
            self.close(403)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data)
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        