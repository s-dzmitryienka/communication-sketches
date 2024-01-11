
from communication_service.notification import Notification


@router(method="POST")
def create_notification(request: Request):
    serializer = NotificationSeriazer(request.data)
    serializer.validate()

    instance: Notification = NotificationRepository.create_notification(serializer.data)
    instance.prepare_and_send()
