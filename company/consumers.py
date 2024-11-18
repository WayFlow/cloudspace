from channels.generic.websocket import AsyncJsonWebsocketConsumer

class CompanyProjectLoggerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if not self.scope.get("projectId") or not self.scope.get("envId"):
            return await self.close(403)
        if not self.scope["user"].is_authenticated:
            return await self.close(401)
        project_log_group = f"{self.scope['projectId']}_{self.scope['envId']}_logs"
        await self.channel_layer.group_add(project_log_group, self.channel_name)
        await self.accept()
        await self.send_json(
            "Started Listening..."
        )

    async def log(self, content):
        await self.send_json(content["message"])
        