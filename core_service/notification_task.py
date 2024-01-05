class NotificationTask(Model):
    status = ChoiceModel([NEW, SENT_TO_SERVICE, SENDING_ERROR])
    
