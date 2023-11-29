class NotificationSenderInterface:
    message: Text
    receiver_contact: Text

    status: Union[NEW, ERROR, DELIVERED]
    status_details: Text

    def __init__(self, notification):
        # init with notification to get access to all provided data to extract only required in each Parent class
        self.notification: Notification = notification

    def _validate(self):
        # validate data like receiver_contact
        # in case if invalid data raise exception and log error
        raise NotImplemented

    def _create_db_instance(self):
        # implement DB record creation to track delivery to communication service, new model?
        ...

    def _send_to_communication_worker(self):
        # implement sending for diff channels
        raise NotImplemented

    @abstractmethod
    def notify(self) -> None:
        self._validate()
        ...  # extract required data, build message?
        self._create_db_instance()
        self._send_to_communication_worker()


class SmsNotificationSender(NotificationInterface):
    receiver_contact: PhoneNumber


class EmailNotificationSender(NotificationInterface):
    receiver_contact: Email
