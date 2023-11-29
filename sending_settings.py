class SendingSettings:
    level: Union[User, Housing, Reservation]
    object_id: UUID

    time_trigger_1_enabled: bool
    time_trigger_2_enabled: bool
    ...

    conditional_trigger_1_enabled: bool
    conditional_trigger_2_enabled: bool
    ...

    def __validate(self):
        """Validates all values in DB to have unique level per object"""
        ...

    @property
    def notification_channels(self):
        return self.notification_channels.all()

    @classmethod
    def get_sending_settings_for_notification(**kwargs) -> Optional[SendingSettings]:
        if object_level_settings := SendingSettings.object.get_one_or_none(
                level=kwargs.get("object_type"),
                level_id=kwargs.get("object_id"),
            )
            return object_level_settings

        if parent_level_settings := SendingSettings.object.get_one_or_none(
                level=kwargs.get("parent_type"),
                level_id=kwargs.get("parent_id"),
            )
            return parent_level_settings