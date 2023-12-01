from abc import abstractmethod

from notification import Notification


class NotificationConditionalProcessorInterface:
    def __init__(self, type, sending_setttings, *args, **kwargs):
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
            Notification(
                type=self.type,
                sending_settings=self.sending_settings,
                receiver_contact=self.get_receiver_contact(),
                message=self.build_message(),
            ).send()


class NotificationConditionalProcessorAfterPayments(NotificationConditionalProcessorInterface):
    def validate(self, *args, **kwargs):
        # check guest_payment instance on __init__ and other required attrs for this class
        ...

    def get_receiver_contact(self, *args, **kwargs) -> bool:
        return ReceiverContact.build_contact_for_reservation(reservation=reservation)

    def build_message(self, *args, **kwargs) -> bool:
        return AbstractMessagesFactory.create_after_payments_complete_message(guest_payment=instance)
    
    def send_if_needed(self, *args, **kwargs) -> bool:
        return True if all conditions passed else False