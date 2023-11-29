class Notification:

    def __init__(self, notification_type: Union[Trigger, TimeCondition]):
        self.notification_type = notification_type
        # pass with parameter or discover from any other instance,
        # e.g: manager user, reservation (we may have independent notifications)
        self.sending_settings = ...

    def _get_handler(self, channel):
        return {
            SMS: SmsNotificationSender,
            EMAIL: EmailNotificationSender,
            ...
            None: DefaultNotification | EmailNotification | Raise Exception Further
        }.get(channel)

    def send(self):
        # 1) Extract required data
        receiver_contact = ...
        # should we build message here?
        # or we can build message in NotificationInterface depends on type and other variables
        message = ...
        # also need to discover type of email, if channel = EMAIL
        # 2) For each enabled channel in sending settings we are calling abstract method to build message, create DB record
        # send notification to communication server
        for channel in self.sending_settings.channels:
            sender = self._get_handler(channel)
            sender(notification=self).notify()