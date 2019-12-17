import json
from logging import getLogger
from dataclasses import asdict

from ..domain import events

logger = getLogger(__name__)


def publish(channel, event: events.Event):
    logger.info("publishing: channel=%s, event=%s", channel, event)
    # r.publish(channel, json.dumps(asdict(event)))
