import json
from unittest.mock import MagicMock, patch
from consumer import callback, PROCESSED_EVENTS

def test_processes_valid_customer_event():
    body = json.dumps({
        "eventId": "evt-1",
        "id": "c1",
        "name": "John Doe"
    }).encode()

    method = MagicMock()
    method.routing_key = "customer.created"
    method.delivery_tag = "tag"

    channel = MagicMock()

    with patch("requests.post") as mock_post:
        callback(channel, method, None, body)

        mock_post.assert_called_once()
        channel.basic_ack.assert_called_once()

def test_skips_duplicate_event():
    PROCESSED_EVENTS.add("evt-dup")

    body = json.dumps({
        "eventId": "evt-dup",
        "id": "c1"
    }).encode()

    method = MagicMock()
    method.routing_key = "customer.created"
    method.delivery_tag = "tag"

    channel = MagicMock()

    callback(channel, method, None, body)

    channel.basic_ack.assert_called_once()
