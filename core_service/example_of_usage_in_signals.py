import typing
from fake_imports import GuestPayment
from core_service.message import AbstractMessagesFactory, Message
from notification import Notification
from core_service.notification_conditional_processors import NotificationConditionalProcessorAfterPayments
from notification_type import NotificationType
from core_service.receiver_contact import ReceiverContact


def post_save_payment_signal(sender, instance: GuestPayment, created: bool, signal, **kwargs):
    ...
    reservation = instance.reservation

    NotificationConditionalProcessorAfterPayments(
        obj=instance,
        sending_settings=reservation.sending_settings,
        type=NotificationType.AFTER_PAYMENTS,
    ).send_if_needed()
