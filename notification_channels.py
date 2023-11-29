class NotificationChannelInterface:
    type: Union[SMS, EMAIL, TELEGRAM]
    sending_settings: SendingSettings(related_name="notification_channels")

    @property
    def provider(self):
        return {
            SMS: SmsProvider,
            EMAIL: EmailProvider,
        }.get(self.type)


    @abstractmethod
    def notify(self, notification: Notification) -> None:
        """
        Sends notification using the special channel type
        """
        ...


class SmsNotificationChannel(NotificationChannelInterface):
    type = SMS

    def __send_sms(self, *args, **kwargs):
        self.provider.send_sms(*args, **kwargs)
    
    def notify(self, notification: Notification) -> None:
        phone, message = notification.contact, notification.message
        return self.__send_sms(phone=phone, message=message)


class EmailNotificationChannel(NotificationChannelInterface):
    type = EMAIL

    def __send_email(self, notification: Notification):
        self.provide.send_email(*args, **kwargs)
    
    def notify(self, *args, **kwargs) -> None:
        email, message = notification.contact, notification.message
        return self.__send_email(email=email, message=message)