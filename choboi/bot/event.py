from dataclasses import dataclass

@dataclass
class Event:
    type: str  # TODO: enum?
    user_id: str

    output = 'slack'


@dataclass
class MessageEvent(Event):
    message: str
    channel: str


@dataclass
class ErrorEvent(Event):
    error: str
    code: str
    message: str


@dataclass
class OutputEvent:
    channel: str
    message: str
