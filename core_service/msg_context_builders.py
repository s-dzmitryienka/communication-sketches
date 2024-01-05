from abc import abstractmethod
from ast import Dict
from typing import Any

from fake_imports import Guest, GuestMembership, GuestPayment, Template

class MessageContextBuilderInterface:
    obj: Any

    @abstractmethod
    def build_context(cls, *args, **kwargs) -> Dict:
        ...


class AfterGuestPaymentsCompleteContextBuilder(MessageContextBuilderInterface):
    
    def __init__(self, guest_payment: GuestPayment) -> None:
        self.obj = guest_payment
        super().__init__()
    
    def build_context(self, *args, **kwargs) -> Dict:
        return {
            "amount": self.obj.amount,
            "housing_name": self.obj.reservation.housing.name,
        }

class AfterGuestRegistrationContextBuilder(MessageContextBuilderInterface):
    
    def __init__(self, guest_membership: GuestMembership, **kwargs) -> None:
        self.obj = guest_membership
    
    def build_context(self, *args, **kwargs) -> Dict:
        return {
            "guest_name": self.obj.guest.full_name,
            "housing_name": self.obj.group.reservation.housing.name,

        }