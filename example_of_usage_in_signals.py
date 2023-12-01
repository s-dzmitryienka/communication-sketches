from fake_imports import GuestPayment
from message import AbstractMessagesFactory, Message
from notification import Notification
from notification_conditional_processors import NotificationConditionalProcessorAfterPayments
from notification_type import NotificationType
from receiver_contact import ReceiverContact


def post_save_payment_signal(sender, instance: GuestPayment, created: bool, signal, **kwargs):
    ...
    reservation = instance.reservation

    NotificationConditionalProcessorAfterPayments(
        obj=instance,
        type=Optional[AfterPayments],
        ending_settings=reservation.sending_settings,
        condition_type=Optional[NotificationType.AFTER_PAYMENTS],

    ).send_if_needed()
