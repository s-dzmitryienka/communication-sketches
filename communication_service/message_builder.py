from communication_service.notification import MessagePayload




class BaseMessageBuilder:
    ...


class TemplatedRenderer:
    def render(self, paylod: dict, template_attr: Enum[EMAIL, SMS]) -> str:
        template = Template.objects.get(unique_template_name=paylod.get("template_name"))
        templated_text = getattr(template, template_attr)
        return jinja.render(templated_text, context=paylod.get("context"))


# class CustomRenderer:
#     def render(self, paylod: dict, template_attr: Enum[EMAIL, SMS]):
#         template = Template.objects.get(unique_template_name=paylod.get("template_name"))
#         templated_text = getattr(template, template_attr)
#         return jinja.render(templated_text, context=context)


class Message(BaseModel):
    type: Enum
    payload: dict

    def get_renderer(self):
        return {
            MessageType.TEMPLATED: TemplatedRenderer,
            MessageType.CUSTOM: CustomRenderer,
        }.get(self.type)

    def render(self, template_attr_name) -> str:
        renderer = self.get_renderer()
        return renderer.render(payload)


class EmailMessageBuilder(BaseMessageBuilder):
    template_attr_name = "html_text"

    def build_from(cls, message_payload: MessagePayload) -> PreparedMessage:
        """
        Message dict format:    
            {
                "type": "TEMPLATED",  # use ENUM
                "payload": {
                    "context": self.context,
                    "template_name": self.template_name,
            }
        """

        raw_message_data: MessagePayload = message_payload.message
        message_obj: Message = Message(**raw_message_data)
        final_message: str = message_obj.render(template_attr_name=cls.template_attr_name)
        return PreparedMessage(final_message=final_message)

        