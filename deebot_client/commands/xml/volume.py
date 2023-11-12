"""Volume command module."""

from typing import Any

from deebot_client.command import InitParam
from deebot_client.event_bus import EventBus
from deebot_client.events import VolumeEvent
from deebot_client.message import HandlingResult, MessageBodyDataDict

from .common import CommandWithMessageHandling, SetCommand


class GetVolume(CommandWithMessageHandling, MessageBodyDataDict):
    """Get volume command."""

    name = "GetVolume"

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """

        event_bus.notify(
            VolumeEvent(volume=data["volume"], maximum=data.get("total", None))
        )
        return HandlingResult.success()

    @classmethod
    def _handle_body_data_xml(
        cls, event_bus: EventBus, xml_message: str
    ) -> HandlingResult:
        raise NotImplementedError


class SetVolume(SetCommand):
    """Set volume command."""

    name = "SetVolume"

    get_command = GetVolume
    _mqtt_params = {
        "volume": InitParam(int),
        "total": None,  # Remove it as we don't can set it (App includes it)
    }

    def __init__(self, volume: int) -> None:
        super().__init__({"volume": volume})