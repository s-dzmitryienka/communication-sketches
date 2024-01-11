from enum import Enum
from communication_service.message_builder import EmailMessageBuilder
from notification import Notification
from notification_channels import NotificationChannelType


class NotificationItemStatus(Enum):
    NEW = "NEW"
    SENT = "SENT"
    ERROR = "ERROR"


class NotificationItem(Model):
    notification: Notification  #FK(Notification)
    channel_type: NotificationChannelType
    status: NotificationItemStatus
    details: str

    attempts: int # [0 - 3]

    def get_msg_builder(self):
        return {
            NotificationChannelType.EMAIL: EmailMessageBuilder,
            NotificationChannelType.SMS: SMSMessageBuilder
        }.get(self.channel_type)

    def get_sender(self):
        return {
            NotificationChannelType.EMAIL: EmailChannelSender,
            NotificationChannelType.SMS: SmsChannelSender
        }.get(self.channel_type)

    def send(self):
        try:
            message_builder: MessageBuilderIntrerface = self.get_msg_builder()
            message: PreparedMessage = message_builder.build_from(message_payload=self.notification.message_payload)
            receiver: ReceiverTypedDict = self.notification.message_payload.receiver

            sender = self.get_sender()
            provider_response = sender.send(receiver=receiver, message=message)
        except Exception as e:
            self.status = "ERROR"
            self.details = str(e)[:256]
        else:
            if provider_response.is_ok:
                self.status = "SENT"
            else:
                self.status = "ERROR"
                self.details = str(provider_response.content)[:256]

        finally:
            self.save()
        
        return self