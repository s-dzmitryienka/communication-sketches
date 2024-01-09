from enum import Enum


class NotificationStatus(Enum):
    NEW = "NEW"
    PARTIALLY_SENT = "PARTIALLY_SENT"
    SENT = "SENT"
    ERROR = "ERROR"
