from dataclasses import dataclass
from typing import Optional
from fake_imports import EmailAddress, PhoneNumber, Reservation


@dataclass
class ReceiverContact:
    phone: Optional[PhoneNumber]
    email: Optional[EmailAddress]

    def validate(self):
        if not any((self.email, self.phone)):
            raise ValueError("Receiver should have at least one contact for communication!!!")

    @classmethod
    def build_contact_for_reservation(cls, reservation: Reservation):
        return cls(
            phone=reservation.default_phone_number,
            email=reservation.default_guest_email,
        )

    @classmethod
    def build_contact_for_guest(cls, guest: Guest):
        return cls(
            phone=guest.phone,
            email=guest.email,
        )
