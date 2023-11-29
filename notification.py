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

