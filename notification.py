class Notification:

    def __init__(self, notification_type: Union[Trigger, TimeCondition]):
        self.notification_type = notification_type
        # pass with parameter or discover from any other instance,
        # e.g: manager user, reservation (we may have independent notifications)
        self.sending_settings = ...

    def _get_interface(self, channel):
        return {
            SMS: SmsNotification,
            EMAIL: EmailNotification,
            ...
            None: DefaultNotification | EmailNotification | Raise Exception Further
        }.get(channel)

    def send(self):
        # 1) Extract required data
        receiver_contact = ...
        # should we build message here?
        # or we can build message in NotificationInterface depends on type and other variables
        message = ...
        # 2) For each enabled channel in sending settings we are calling abstract method to build message, create DB record
        # send notification to communication server
        for channel in self.sending_settings.channels:
            interface = self._get_interface(channel)
            interface(receiver_contact, message, ...).notify()


class NotificationInterface:
    channels: NotificationChannelInterface
    message: Text
    receiver_contact: Text
    
    status: Union[NEW, ERROR, DELIVERED]
    status_details: Text


    @abstractmethod
    def notify_in_all_channels(self) -> None:
        """
        Sends notification using each channel type associated in settings
        """
        for channel in notification.channels:
            channel.notify()


# class SmsNotification(NotificationInterface):
#     receiver_contact: PhoneNumber

# class EmailNotification(NotificationInterface):
#     receiver_contact: Email

