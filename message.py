from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from fake_imports import GuestMembership, GuestPayment, Template, render_html_text, render_plain_text
from msg_context_builders import AfterGuestPaymentsCompleteContextBuilder, AfterGuestRegistrationContextBuilder, MessageContextBuilderInterface


@dataclass
class Message:
    template_id: Optional[UUID]
    html_text: Optional[str]
    plain_text: Optional[str]
    context_builder: MessageContextBuilderInterface

    def validate(self):
        template = Template.objects.get_one_or_none(id=self.template_id)
        if not any((template, self.html_text, self.plain_text)):
            raise ValueError("Message can not be empty!")
    
    @property
    def prepare_html_text(self) -> str:
        if self.html_text:
            return self.html_text
        
        template = Template.objects.get_one_or_none(id=self.template_id)
        if template:
            context: dict = self.context_builder.build_context()
            html_text = render_html_text(template, context)
            return html_text
        
        return self.plain_text
    
    @property
    def prepare_plain_text(self) -> str:
        template = Template.objects.get_one_or_none(id=self.template_id)
        if template:
            context: dict = self.context_builder.build_context()
            plain_text = render_plain_text(template, context)
            return plain_text
        
        return self.plain_text


class AbstractMessagesFactory:

    @classmethod
    def create_after_payments_complete_message(cls, guest_payment: GuestPayment) -> Message:
        return Message(
            template_id=Template.objects.get_one_or_none(unique_name="AFTER_PAYMENTS_COMPLETE"),  # todo: move to Enum
            context_builder=AfterGuestPaymentsCompleteContextBuilder(guest_payment=guest_payment),
        )

    @classmethod
    def create_after_guest_registration_message(cls, guest_membership: GuestMembership) -> Message:
        return Message(
            template_id=Template.objects.get_one_or_none(unique_name="AFTER_GUEST_REGISTRATION"),  # todo: move to Enum
            context_builder=AfterGuestRegistrationContextBuilder(guest_membership=guest_membership),
        )