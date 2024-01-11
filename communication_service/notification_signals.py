# def notification_signals(instance: Notification, sender: Notification):
#     if created:
#         instance.send()


def notification_item_signals(instance: NotificationItem, sender: NotificationItem):
    recalculate_notification_generic_status(instance)


def recalculate_notification_generic_status(notification_item):
    notification = notification_item.notification
    general_status = notification.calc_general_status()
    notification.general_status = general_status
    notification.save()