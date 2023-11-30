from fake_imports import GuestPayment
from message import AbstractMessagesFactory, Message
from notification import Notification
from notification_type import NotificationType
from receiver_contact import ReceiverContact


def post_save_payment_signal(sender, instance: GuestPayment, created: bool, signal, **kwargs):
    ...
    reservation = instance.reservation
    Notification(
        type=NotificationType.AFTER_PAYMENTS,
        sending_settings=reservation.sending_settings,
        receiver_contact=ReceiverContact.build_contact_for_reservation(reservation=reservation),
        message=AbstractMessagesFactory.create_after_payments_complete_message(guest_payment=instance)
    ).send()
