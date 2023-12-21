from abc import abstractmethod
from enum import Enum
from uuid import UUID
from message import Message
from notification_status import NotificationStatus
from notification_type import NotificationType
from receiver_contact import ReceiverContact
from sending_settings import SendingSettings


class NotificationLinkedObjectClassifier(Enum):
    RESERVATION = "RESERVATION"
    GUEST_PAYMENT = "GUEST_PAYMENT"


class Notification:
    """
    Notification:
	- NotificationItem(SMS): ID -> redis ID: JSON
		- delieverySms:
			attempt1
			attempt2 
	- NotificationItem(EMAIL) -> redis ID: JSON
		- delieveryEmail:
			attempt1
			attempt2 
	- NotificationItem(WhatsUp) -> redis ID: JSON
		- delieveryWhatsUp:
			attempt1
			attempt2 
    """
    linked_object_id: UUID
    linked_object_type: NotificationLinkedObjectClassifier

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
