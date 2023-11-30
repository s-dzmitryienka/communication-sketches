class SendingSettings:
    level: Union[User, Housing, Reservation]
    object_id: UUID

    time_trigger_1_enabled: bool
    time_trigger_2_enabled: bool
    ...

    conditional_trigger_1_enabled: bool
    conditional_trigger_2_enabled: bool
    ...
