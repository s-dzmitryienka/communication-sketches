from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from fake_imports import GuestMembership, GuestPayment, Template, render_html_text, render_plain_text
from core_service.msg_context_builders import AfterGuestPaymentsCompleteContextBuilder, AfterGuestRegistrationContextBuilder, MessageContextBuilderInterface


class MessageInterface(ABC):
    
    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def build_message_pack(self) -> dict:
        ...


@dataclass
class TemplatedMessage(MessageInterface):
    template_name: str
    context: dict
    
    def build_message_pack(self) -> dict:
        return {
            "type": "TEMPLATED",  # use ENUM
            "payload": {
                "context": self.context,
                "template_name": self.template_name,
            }
        }


@dataclass
class RawMessage(MessageInterface):
    body: str

    def validate(self):
        if not self.body:
            raise ValueError("Message can not be empty!")
    
    def build_message_pack(self) -> dict:
        return {
            "type": "RAW",  # use ENUM
            "payload": {
                "body": self.body,
            }
        }


class AbstractMessagesFactory:

    @classmethod
    def create_after_payments_complete_message(cls, guest_payment: GuestPayment) -> MessageInterface:
        return TemplatedMessage(
            template_name="AFTER_PAYMENTS_COMPLETE",  # todo: move to Enum
            context=AfterGuestPaymentsCompleteContextBuilder(guest_payment=guest_payment).build_context(),
        )

    @classmethod
    def create_after_guest_registration_message(cls, guest_membership: GuestMembership) -> MessageInterface:
        return TemplatedMessage(
            template_name="AFTER_GUEST_REGISTRATION",  # todo: move to Enum
            context=AfterGuestRegistrationContextBuilder(guest_membership=guest_membership).build_context(),
        )