from enum import Enum
from notification import Notification
from notification_channels import NotificationChannelType


class NotificationStatus(Enum):
    NEW = "NEW"
    READY_TO_SEND = "READY_TO_SEND"  # msg body stored to NOSQL
    SENT = "SENT"
    ERROR = "ERROR"


class NotificationItem(Model):
    notification: FK(Notification)
    channel: NotificationChannelType
    status: NotificationStatus

    @property
    def no_sql_provider(self):
        storage_name = settings.DEFAULT_NOSQL_STORAGE
        {
            "REDIS": RedisCli(...)
            "MONGO_DB": MongoCli(...)
        }.get(storage_name)

    @property
    def message_body(self):
        """
        In NOSQL table structure will be as
            id1: JSON 1
            id2: JSON 2
            ...
        """
        return self.no_sql_provider.get(self.id.hex)
