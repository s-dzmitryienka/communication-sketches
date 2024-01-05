class AbstractNotificationSender(ABC):
    @abstractmethod
    def send():
        ...


class EmailChannelSender(AbstractNotificationSender):
    def send(...):
        email_provider.send()



class SmsChannelSender(AbstractNotificationSender):
    def send(...):
        sms_provider.send()