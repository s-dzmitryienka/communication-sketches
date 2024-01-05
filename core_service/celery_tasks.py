class NotificationServiceSenderTask(celery.Task):
    def run(task_id):
        task = NotificationTask.objects.get(id=task_id)
        payload = task.prepare_payload()
        response = srv_cli.create_notification(payload)
        
        if response.status_code == 201:
            task.set_status("SENT_TO_SERVICE")
        else:
            task.status = "ERROR"
            task.status_details = str(response.content)[:512]
            task.save()