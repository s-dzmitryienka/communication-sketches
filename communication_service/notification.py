from abc import abstractmethod
from dataclasses import dataclass
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


@dataclass
class MessagePayload:
    linked_object_id: UUID
    linked_object_type: ENUM
    type: ENUM
    message: MessageTypedDict
    receiver: ReceiverTypedDict
    sending_settings: SendingSettignsTypedDict


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
    id: UUID
    linked_object_id: UUID
    linked_object_type: NotificationLinkedObjectClassifier

    notification_task_id: UUID  # we can get this task from NoSQL and serialize it into some dataclass

    n_type: NotificationType
    
    general_status: NotificationStatus
    status_details: str

    @property
    def message_payload(self) -> MessagePayload:
        """
        Have possibility to deserialize to some dataclass MessagePayload.

        Expected format:
            {
                "linked_object_id": uuid,
                "linked_object_type": str,
                "type": str,
                "message": dict,
                "receiver": dict,
                "sending_settings": dict
            }

        Message dict format:    
            {
                "type": "TEMPLATED",  # use ENUM
                "payload": {
                    "context": self.context,
                    "template_name": self.template_name,
            }
        
        Receiver contact dict format:
            {
                "phone": "+92837928",
                "email": "lee@ls.com"
            }
        """
        raw_dict = self.nosql_storage.get(self.notification_task_id)
        return MessagePayload(**raw_dict)

    @property
    def sending_settings(self) -> dict:
        msg: MessagePayload = self.message_payload
        return msg.sending_settings

    def prepare_and_send(self) -> None:
        """
        Sends notification using each channel type associated in settings
        """
        
        if self.sending_settings.is_email_channel_enabled:
            email_notification_item: NotificationItem = NotificationItem.objects.create(
                channel_type="EMAIL",
                notification=self,
                )
            NotificationItemEmailSenderCeleryTask.delay(email_notification_item.id)

        if self.sending_settings.is_sms_channel_enabled:
            sms_notification_item: NotificationItem = NotificationItem.objects.create(
                channel_type="SMS",
                notification=self,
                )
            NotificationItemSMSSenderCeleryTask.delay(sms_notification_item.id)
