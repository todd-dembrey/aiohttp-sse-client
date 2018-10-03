#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from aiohttp_sse_client import client as sse_client

from .const import WPT_SERVER


async def test_eventsource_close():
    """Test EventSource: close.
    
    ..seealso: https://github.com/web-platform-tests/wpt/blob/master/
    eventsource/eventsource-close.htm
    """
    source = sse_client.EventSource(WPT_SERVER + 'resources/message.py')
    assert source.ready_state == sse_client.READY_STATE_CONNECTING
    await source.connect()
    assert source.ready_state == sse_client.READY_STATE_OPEN
    await source.close()
    assert source.ready_state == sse_client.READY_STATE_CLOSED


async def test_eventsource_close_reconnect():
    """Test EventSource: close/reconnect.
    
    ..seealso: https://github.com/web-platform-tests/wpt/blob/master/
    eventsource/eventsource-close.htm
    """
    count = 0
    reconnected = False
    
    def on_error():
        nonlocal count, reconnected
        if count == 1:
            assert source2.ready_state == sse_client.READY_STATE_CONNECTING
            reconnected = True
        elif count == 2:
            assert source2.ready_state == sse_client.READY_STATE_CONNECTING
            count += 1
        elif count == 3:
            assert source2.ready_state == sse_client.READY_STATE_CLOSED
        else:
            assert False
    
    async with sse_client.EventSource(
        WPT_SERVER + 'resources/reconnect-fail.py?id=' +
        str(datetime.utcnow().timestamp()),
        reconnection_time=timedelta(milliseconds=2),
        on_error=on_error
    ) as source2:
        async for e in source2:
            if count == 0:
                assert reconnected is False
                assert e.data == "opened"
            elif count == 1:
                assert reconnected is True
                assert e.data == "reconnected"
            else:
                assert False
            count += 1