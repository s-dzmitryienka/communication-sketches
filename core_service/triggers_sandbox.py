from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeVar


Observer = TypeVar("Observer")

### ------------------ Subjects --------------------

class TriggerSubjectInterface(ABC):

    _observers: List[Observer] = []

    @classmethod
    def attach(cls, observer: Observer) -> None:
        cls._observers.append(observer)

    @classmethod
    def detach(cls, observer: Observer) -> None:
        cls._observers.remove(observer)

    @classmethod
    def notify(cls, msg: str) -> None:
        for observer in cls._observers:
            observer.on_event(msg)


class AfterPaymentCompleteTriggerSubject(TriggerSubjectInterface):

    @classmethod
    def on_event(cls, msg: str) -> None:
        cls.notify(msg)

### ------------------ Observers --------------------

class EventObserverInterface(ABC):

    @abstractmethod
    def on_event(cls, msg: str) -> None:
        pass


class AterPaymentsCommunicationEventObserver(EventObserverInterface):
    
    @classmethod
    def on_event(cls, msg: str) -> None:
        print(f"[AterPaymentsCommunicationEventObserver]: process message: {msg}")


class AterPaymentsWebhookEventObserver(EventObserverInterface):
    
    @classmethod
    def on_event(cls, msg: str) -> None:
        print(f"[AterPaymentsWebhookEventObserver]: process message: {msg}")

### ------------------ Subscriptions ------------------
### subscribes the observers somewhere on the module level
AfterPaymentCompleteTriggerSubject.attach(AterPaymentsCommunicationEventObserver)
AfterPaymentCompleteTriggerSubject.attach(AterPaymentsWebhookEventObserver)


### -------------------Example of usage ---------------
AfterPaymentCompleteTriggerSubject.on_event("guest payment Complete")
"""
Out:
    [AterPaymentsCommunicationEventObserver]: process message: guest payment Complete
    [AterPaymentsWebhookEventObserver]: process message: guest payment Complete
"""