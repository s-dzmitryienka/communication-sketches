class NotificationTask(Model):
    id: UUID
    linked_object_id: UUID
    linked_object_type: ENUM
    n_type: ENUM,
    status = ChoiceModel([NEW, SENT_TO_SERVICE, SENDING_ERROR])
    
