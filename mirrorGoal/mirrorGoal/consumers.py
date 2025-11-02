from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close(code=4001, reason="login required")
            return
        
        self.user = user
        self.threads = await self.get_user_threads(user)   # ✅ await DB call

        # Join all user threads
        for thread in self.threads:
            await self.channel_layer.group_add(
                f"chat_{thread.id}",
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        for thread in getattr(self, "threads", []):
            await self.channel_layer.group_discard(
                f"chat_{thread.id}",
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        action_type = content.get("type")
        thread_id = content.get("thread_id")                                                   

        if action_type == "send_message":
            sender_id = self.scope['user'].id
            message_text = content.get("text")

            # ✅ don’t use self.thread_id (it wasn’t set) → use the one from content                                                                                                                                                                                                                                                                                            
            message = await self.save_message(sender_id, thread_id, message_text)

            if message:
                await self.channel_layer.group_send(
                    f"chat_{thread_id}",
                    {
                        "type": "chat_message",
                        "sender": sender_id,
                        "message": {
                            "id": message.id,
                            "sender": {
                                "id": message.sender.id,
                                "username": message.sender.username
                            },
                            "text": message_text,
                            "sent_at": str(message.sent_at),
                            "status": message.status,
                            "thread_id": thread_id
                        }
                    }
                )

        elif action_type == "update_status":
            message_id = content.get("message_id")
            new_status = content.get("status")

            message_data = await self.update_message_status(message_id, new_status)

            if message_data:
                await self.channel_layer.group_send(
                    f"chat_{message_data['thread_id']}",
                    {
                        "type": "message_status_update",
                        "message_id": message_data["id"],
                        "status": message_data["status"],
                        "thread_id": message_data["thread_id"],
                    }
                )

        elif action_type == "join_thread":
            # ✅ Add this user’s socket to the thread group
            await self.channel_layer.group_add(
                f"chat_{thread_id}",
                self.channel_name
            )

            # ✅ Optionally send previous messages for this thread
            previous_messages = await self.get_previous_messages(thread_id)
            await self.send_json({
                "type": "chat_history",
                "thread_id": thread_id,
                "messages": [
                    {
                        "id": msg.id,
                        "sender": {
                            "id": msg.sender.id,
                            "username": msg.sender.username
                        },
                        "text": msg.text,
                        "sent_at": str(msg.sent_at),
                        "status": msg.status,
                    }
                    for msg in previous_messages
                ]
            })


    async def chat_message(self, event):
        await self.send_json(event)

    async def message_status_update(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def update_message_status(self, message_id, new_status):
        from .models import Message
        try:
            msg = Message.objects.get(id=message_id)
            msg.status = new_status
            msg.save(update_fields=["status"])
            # ✅ return a dict, not a model (so no lazy DB calls later)
            return {
                "id": msg.id,
                "status": msg.status,
                "thread_id": msg.thread_id,  # use FK id directly
            }
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender_id, thread_id, text):
        from .models import Message, MessageThread
        thread = MessageThread.objects.get(id=thread_id)
        sender = User.objects.get(id=sender_id)
        return Message.objects.create(thread=thread, sender=sender, text=text)

    @database_sync_to_async
    def get_previous_messages(self, thread_id):
        from .models import Message   # ✅ import here
        # thread = MessageThread.objects.get(id=thread_id)
        return list(Message.objects.filter(thread_id=thread_id).order_by("sent_at").select_related("sender"))

    @database_sync_to_async
    def get_user_threads(self, user):
        from .models import MessageThread   # ✅ import here
        return list(MessageThread.objects.filter(participants=user))

    @database_sync_to_async
    def get_other_participant_name(self, thread, user):
        others = thread.participants.exclude(id=user.id)
        if others.exists():
            return others.first().username  # or .get_full_name()
        return "Unknown"