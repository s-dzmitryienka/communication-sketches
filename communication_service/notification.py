from abc import abstractmethod
from enum import Enum
from uuid import UUID
from core_service.message import Message
from notification_status import NotificationStatus
from notification_type import NotificationType
from core_service.receiver_contact import ReceiverContact
from core_service.sending_settings import SendingSettings


class NotificationLinkedObjectClassifier(Enum):
    RESERVATION = "RESERVATION"
    GUEST_PAYMENT = "GUEST_PAYMENT"


class Notification(Model):
    """
    Notification:
	- NotificationItem(SMS): ID -> dynamoDB ID: JSON
		- delieverySms:
			attempt1
			attempt2 
	- NotificationItem(EMAIL) -> dynamoDB ID: JSON
		- delieveryEmail:
			attempt1
			attempt2 
	- NotificationItem(WhatsUp) -> dynamoDB ID: JSON
		- delieveryWhatsUp:
			attempt1
			attempt2 
    ++
    Set TTL for record in dynamoDB (3 months) and try to connect Lambda to patch service about the JSON related with the
    message was automatically delete by dynamodb, to have actual state about stored JSONs related with notification 
    instance.

    """
    linked_object_id: UUID
    linked_object_type: NotificationLinkedObjectClassifier

    notification_task_id: UUID  # we can get this task from NoSQL and serialize it into some dataclass

    type: NotificationType
    sending_settings_id: UUID  # maybe store SendingSettings JSON obj in NoSQL and retrieve it during sending
    
    message: Message
    receiver_contact: ReceiverContact
    
    status: NotificationStatus
    status_details: str

    @abstractmethod
    def send(self) -> None:
        """
        Sends notification using each channel type associated in settings
        """
        # sending_settings = core_cli.get_sending_settings(self.sending_settings_id)
        # or sending_settings = dynamodb.get_sending_settings(self.sending_settings_id)

        if sending_settings.is_email_channel_enabled:
            EmailChannelSender.send(self.receiver_contact, self.message)

        if sending_settings.is_sms_channel_enabled:
            SMSChannelSender.send(self.receiver_contact, self.message)