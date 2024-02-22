from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Observer: pass


class TriggerSubjectInterface(ABC):

    _observers: List[Observer] = []

    @classmethod
    def attach(cls, observer: Observer) -> None:
        cls._observers.append(observer)

    @classmethod
    def detach(cls, observer: Observer) -> None:
        cls._observers.remove(observer)

    @classmethod
    def notify(cls, event: Event) -> None:
        for observer in cls._observers:
            observer.on_event(event)


class AfterPaymentCompleteTrigger(TriggerSubjectInterface):

    def on_event(self, guest_payment: "GuestPayment") -> None:
        event = Event(
            ev_type=EVENT_TYPE.AfterPaymentComplete
            related_instance=guest_payment,
            ...
        )
        self.notify(event)


class EventObserverInterface(ABC):

    @abstractmethod
    def on_event(self, event: Type[Event]) -> None:
        pass


class AterPaymentsCommunicationEventObserver(EventObserverInterface):
    def on_event(self, event: Type[Event]) -> None:
        NotificationConditionalProcessorAfterPayments(
                obj=event.related_instance,
                sending_settings=event.related_instance.reservation.sending_settings,
                type=NotificationType.AFTER_PAYMENTS,
            ).send_if_needed()


class AterPaymentsWebhookEventObserver(EventObserverInterface):
    def on_event(self, event: Type[Event]) -> None:
        Webhook.send({
            "type": "PAYMENTS_COMPLETE",
            ""
        })