class SendingSettings:  # Existing model
    level: Union[User, Housing, Reservation]
    object_id: UUID

    is_email_channel_enabled: bool (default=True)  # new field
    is_sms_channel_enabled: bool (default=False)  # new field

    time_trigger_1_enabled: bool
    time_trigger_2_enabled: bool
    ...

    conditional_trigger_1_enabled: bool
    conditional_trigger_2_enabled: bool
    ...


# TODO:
    # - add unique Flag for each relationship User/Housing/Reservation to have only one setting
    # - add new endpoint to update sending-settings to avoid updating housing/user level settings from reservation level 


# ------------------------------------------------------------------------------------------------------------------
### If for each channel we will use separated settings
class AbstactSendingSettings:
    type: ChoiceField[SMS, EMAIL]

    time_trigger_1_enabled: bool
    time_trigger_2_enabled: bool
    ...

    conditional_trigger_1_enabled: bool
    conditional_trigger_2_enabled: bool

    class Meta:
        abstract = True
        unuque_together = ((type, user), (type, reservation), (type, housing))


class EmailSendingSettings(AbstactSendingSettings):
    type = EMAIL
    ...

class SMSSendingSettings(AbstactSendingSettings):
    type = SMS
    ...