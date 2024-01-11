from communication_service.notification_item import NotificationItem


class NotificationItemSenderCeleryTask:
    ...


class NotificationItemSenderCeleryTask(NotificationItemSenderCeleryTask):
    def run(notification_item_id: UUID):
        notification_item: NotificationItem = NotificationItem.get_by_id(id=notification_item_id)
        notification_item.send()
