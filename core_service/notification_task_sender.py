from abc import ABC
from typing import Type
from uuid import UUID
from core_service.celery_tasks import NotificationServiceSenderTask
from core_service.message import MessageInterface
from core_service.notification_task import NotificationTask
from core_service.receiver_contact import ReceiverContact
from fake_imports import transaction
from nosql_storage import DynamoDBStorage, NoSQLStorageInterface, get_nosql_storage
from notification_type import NotificationType

nosql_storage: NoSQLStorageInterface = get_nosql_storage()


class NotificationTaskSenderProcessorInterface(ABC):
    storage: NoSQLStorageInterface = nosql_storage

    def __init__(
            self,
            *,
            linked_object_id: UUID,
            linked_object_type: str,
            n_type: NotificationType,
            sending_settings_id: UUID,
            receiver_contact: ReceiverContact,
            message: Type[MessageInterface],
    ):
        self.linked_object_id =  linked_object_id
        self.linked_object_type = linked_object_type
        self.n_type = n_type
        self.sending_settings_id = sending_settings_id
        self.receiver_contact = receiver_contact
        self.message = message

    
    def build_notification_task_data(self) -> dict:
        """
        Prepares jsonable version of notification task data for saving it in NoSQL storage

        Expected format:
            {
                "linked_object_id": uuid,
                "linked_object_type": str,
                "type": str,
                "message": dict,
                "receiver": dict,
                "sending_settings": dict
            }
        """
        msg: dict = self.message.build_message_pack()
        receiver: dict = self.receiver_contact.to_jsonable()
        sending_settings_obj = SendingSettings.objects.get(id=self.sending_settings_id)
        return {
                "linked_object_id": self.linked_object_id,
                "linked_object_type": self.linked_object_type,
                "type": self.type,
                "message": msg,
                "receiver": receiver,
                "sending_settings": sending_settings_obj.__dict__,
        }

    def store_payload(self, key: UUID, payload: dict):
        self.storage.set(key, payload)  # TTL ~3 months

    def create_task_and_send(self):
        payload = self.build_notification_task_data()
        task = NotificationTask.objects.create(
            linked_object_id=self.linked_object_id,
            linked_object_type=self.linked_object_type,
            n_type=self.n_type,
            status="NEW"
        )
        try:
            self.store_payload(key=task.id, payload=payload)
        except Exception as e:
            task.set_error(e)
        else:
            NotificationServiceSenderTask.delay(task.id)  # or maybe it's better to use worker as sender to service


class NotificationTaskSenderProcessor(NotificationTaskSenderProcessorInterface):
    pass
