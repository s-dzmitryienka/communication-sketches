from abc import abstractmethod
from enum import Enum
from fake_imports import EmailProvider, SmsProvider
from core_service.message import Message
from core_service.receiver_contact import ReceiverContact

from core_service.sending_settings import SendingSettings


class NotificationChannelType(Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"


class NotificationChannelInterface:
    type: NotificationChannelType
    sending_settings: SendingSettings(related_name="notification_channels")

    @property
    def provider(self):
        return {
            NotificationChannelType.SMS: SmsProvider,
            NotificationChannelType.EMAIL: EmailProvider,
        }.get(self.type)

    @abstractmethod
    def send(self, receiver_contact: ReceiverContact, message: Message) -> None:
        """
        Sends notification using the special channel type
        """
        ...


class SmsNotificationChannel(NotificationChannelInterface):
    type = NotificationChannelType.SMS

    def __send_sms(self, *args, **kwargs):
        self.provider.send_sms(*args, **kwargs)
    
    def send(self, receiver_contact: ReceiverContact, message: Message) -> None:
        msg = message.prepare_plain_text()
        return self.__send_sms(phone=receiver_contact.phone, message=msg)


class EmailNotificationChannel(NotificationChannelInterface):
    type = NotificationChannelType.EMAIL

    def __send_email(self, *args, **kwargs):
        self.provider.send_email(*args, **kwargs)
    
    def send(self, receiver_contact: ReceiverContact, message: Message) -> None:
        msg = message.prepare_html_text()
        return self.__send_email(email=receiver_contact.email, message=msg)
