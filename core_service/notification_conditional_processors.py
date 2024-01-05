from abc import abstractmethod
from typing import Type
from core_service.notification_task_sender import NotificationTaskSenderProcessor
from fake_imports import GuestPayment, GuestPaymentStatus
from core_service.message import AbstractMessagesFactory, MessageInterface

from notification import Notification
from core_service.receiver_contact import ReceiverContact


class NotificationConditionalProcessorInterface:
    def __init__(self, obj, type, sending_setttings: "SendingSettings", *args, **kwargs):
        self.obj = obj
        self.type=type
        self.sending_settings = sending_setttings

        self.validate(type, sending_setttings, *args, **kwargs)

    @abstractmethod
    def validate(self, *args, **kwargs):
        ...
    
    @abstractmethod
    def should_send(self, *args, **kwargs) -> bool:
        raise NotImplemented
    
    @abstractmethod
    def get_receiver_contact(self, *args, **kwargs) -> bool:
        raise NotImplemented
    
    @abstractmethod
    def build_message(self, *args, **kwargs) -> bool:
        raise NotImplemented
    
    @abstractmethod
    def send_if_needed(self, *args, **kwargs) -> bool:
        if self.should_send():
            task_sender_processor = NotificationTaskSenderProcessor(
                linked_object_id=self.obj.id,
                linked_object_type=self.obj.__class__.__name__,
                n_type=self.type,
                sending_settings_id=self.sending_settings.id,
                receiver_contact=self.get_receiver_contact(),
                message=self.build_message(),
            )
            task_sender_processor.create_task_and_send()


class NotificationConditionalProcessorAfterPayments(NotificationConditionalProcessorInterface):

    
    def validate(self, *args, **kwargs):
        assert type(self.obj) is GuestPayment, f"Wrong object type for {self.__class__.__name__}!"

    def get_receiver_contact(self, *args, **kwargs) -> ReceiverContact:
        return ReceiverContact.build_contact_for_reservation(reservation=self.obj.reservation)

    def build_message(self, *args, **kwargs) -> Type[MessageInterface]:
        return AbstractMessagesFactory.create_after_payments_complete_message(guest_payment=self.obj)
    
    def _are_all_conditions_satisfy(self):
        if self.obj.status is GuestPaymentStatus.COMPLETE:
            return True
        return False
    
    def should_send(self, *args, **kwargs) -> bool:
        return self._are_all_conditions_satisfy()
