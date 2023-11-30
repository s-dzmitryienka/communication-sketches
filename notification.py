from abc import abstractmethod
from message import Message
from notification_status import NotificationStatus
from notification_type import NotificationType
from receiver_contact import ReceiverContact
from sending_settings import SendingSettings


class Notification:
    type: NotificationType
    sending_settings: SendingSettings
    
    message: Message
    receiver_contact: ReceiverContact
    
    status: NotificationStatus
    status_details: str

    @abstractmethod
    def send(self) -> None:
        """
        Sends notification using each channel type associated in settings
        """
        for channel in self.sending_settings.channels:
            channel.send(self.receiver_contact, self.message)
